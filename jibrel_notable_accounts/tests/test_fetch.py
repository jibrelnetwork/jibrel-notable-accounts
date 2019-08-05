from asyncio import AbstractEventLoop
from concurrent.futures.thread import ThreadPoolExecutor

import pytest

import requests
from requests_mock import Mocker

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.parser.utils import http
from jibrel_notable_accounts.tests.plugins.types import SettingsOverrider


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_fetch_request_to_the_base_url_comes_through_proxy(
        requests_mock: Mocker,
        loop: AbstractEventLoop,
        executor: ThreadPoolExecutor,
) -> None:
    requests_mock.register_uri('GET', settings.ES_BASE_URL, text='42')

    await http.fetch(settings.ES_BASE_URL, loop, executor)

    assert requests_mock.last_request.proxies['https'] == 'https://user:pass@0.proxy.com:0'


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_fetch_proxies_gets_cycled(
        requests_mock: Mocker,
        loop: AbstractEventLoop,
        executor: ThreadPoolExecutor,
) -> None:
    requests_mock.register_uri('GET', settings.ES_BASE_URL, text='42')

    proxy_hosts_cycle = [f'https://user:pass@{x}.proxy.com:{x}' for x in range(len(settings.PROXY_LIST))]
    proxy_hosts_cycles = proxy_hosts_cycle + proxy_hosts_cycle

    for proxy_host in proxy_hosts_cycles:
        await http.fetch(settings.ES_BASE_URL, loop, executor)
        assert requests_mock.last_request.proxies['https'] == proxy_host


async def test_fetch_chooses_user_agent(
        override_settings: SettingsOverrider,
        requests_mock: Mocker,
        loop: AbstractEventLoop,
        executor: ThreadPoolExecutor,
) -> None:

    user_agent = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    )

    override_settings('USER_AGENT_LIST', [user_agent])

    requests_mock.register_uri('GET', settings.ES_BASE_URL, text='42')
    await http.fetch(settings.ES_BASE_URL, loop, executor)

    assert requests_mock.last_request.headers['User-Agent'] == user_agent


@pytest.mark.usefixtures('mock_sleepers')
async def test_fetch_returns_none_if_response_code_is_not_200(
        requests_mock: Mocker,
        loop: AbstractEventLoop,
        executor: ThreadPoolExecutor,
) -> None:
    requests_mock.register_uri('GET', settings.ES_BASE_URL, status_code=500)
    response = await http.fetch_or_return_none(settings.ES_BASE_URL, loop, executor)

    assert response is None


async def test_fetch_returns_response_text_if_response_code_is_200(
        requests_mock: Mocker,
        loop: AbstractEventLoop,
        executor: ThreadPoolExecutor,
) -> None:
    requests_mock.register_uri('GET', settings.ES_BASE_URL, status_code=200, text='42')
    response = await http.fetch_or_return_none(settings.ES_BASE_URL, loop, executor)

    assert response == '42'


@pytest.mark.usefixtures('mock_sleepers')
async def test_fetch_retries_if_exception_occurred(
        requests_mock: Mocker,
        loop: AbstractEventLoop,
        executor: ThreadPoolExecutor,
) -> None:
    requests_mock.register_uri('GET', settings.ES_BASE_URL, exc=requests.exceptions.ConnectTimeout)

    try:
        await http.fetch(settings.ES_BASE_URL, loop, executor)
    except requests.exceptions.ConnectTimeout:
        # In the end, `backoff` raises suppressed error.
        pass

    assert len(requests_mock.request_history) == settings.HTTP_FETCH_MAX_RETRIES
