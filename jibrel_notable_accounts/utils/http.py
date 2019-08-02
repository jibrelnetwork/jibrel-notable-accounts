import asyncio
import logging
import random
from concurrent import futures

import backoff
import requests
from typing import Optional, Dict

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.utils.proxy import get_cooled_proxy

logger = logging.getLogger(__name__)


class InvalidStatusCode(requests.RequestException):
    pass


async def fetch(url: str, loop: asyncio.AbstractEventLoop, executor: futures.Executor) -> str:
    # WTF: `aiohttp` cannot proxy over HTTPS right now, see:
    # https://github.com/aio-libs/aiohttp/issues/845.

    return await loop.run_in_executor(executor, fetch_sync, url)


async def fetch_or_return_none(
        url: str,
        loop: asyncio.AbstractEventLoop,
        executor: futures.Executor,
) -> Optional[str]:

    try:
        return await fetch(url, loop, executor)
    except requests.RequestException:
        logger.exception("URL fetching error")

    return None


@backoff.on_exception(backoff.expo, max_tries=settings.HTTP_FETCH_MAX_RETRIES, exception=requests.RequestException)
def fetch_sync(url: str) -> str:
    logger.debug("Fetching...", extra={"url": url})

    proxy = get_cooled_proxy()
    user_agent = get_random_user_agent()

    try:
        response = perform_fetch_sync(url, proxies={"https": proxy.host}, headers={"User-Agent": user_agent})
    except Exception:
        proxy.write_failure()
        raise

    proxy.write_success()

    logger.debug("Fetched", extra={"url": url})

    return response.text


def perform_fetch_sync(url: str, proxies: Dict[str, str], headers: Dict[str, str]) -> requests.Response:
    response = requests.get(url, proxies=proxies, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        raise InvalidStatusCode(f"'{url}' responded with a status '{response.status_code}' instead of '200'")

    return response


def get_random_user_agent() -> str:
    return random.choice(settings.USER_AGENT_LIST).strip()
