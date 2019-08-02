import asyncio
import collections

import functools
import logging
import operator

import backoff
import mode

from concurrent import futures
from typing import List, Any, Tuple, DefaultDict, Dict, Set

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.parser.utils import parsing
from jibrel_notable_accounts.parser.utils import http

from jibrel_notable_accounts.parser.utils.structs import AccountList, NotableAccount, RawNotableAccount

logger = logging.getLogger(__name__)


class ParserService(mode.Service):
    FIRST_PAGE_NUMBER = 1

    ACCOUNTS_LIST_URL_XPATH = "//div[@class='dropdown']/div/a[contains(text(), 'Accounts')]"
    ACCOUNT_ROW_XPATH = "//table/tbody/tr[td and not(td/div[text() = 'There are no matching entries'])]"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.executor = futures.ThreadPoolExecutor(max_workers=settings.REQUESTS_MAX_WORKERS)

    @mode.Service.task
    async def parse(self) -> None:
        while not self.should_stop:
            await self.parse_once()
            await asyncio.sleep(settings.NOTABLE_ACCOUNTS_PARSE_ONCE_DELAY)

    @backoff.on_exception(backoff.fibo, max_tries=5, exception=Exception)
    async def parse_once(self) -> int:
        logger.info("Parsing notable accounts...")

        accounts_lists = await self.get_accounts_lists()
        accounts = await self.get_accounts(accounts_lists)

        await self.write_accounts(accounts)

        return len(accounts)

    async def get_accounts_lists(self) -> List[AccountList]:
        logger.info("Parsing lists of notable accounts...")

        lists = list()

        # WTF: `fetch_async` instead of `fetch_or_return_none_async` is
        # intentional. This is an entrypoint for `parse_once` and if Proxies
        # die 5 times in a row, service will crash and container will be
        # restarted.
        html = await http.fetch(settings.ES_LABEL_CLOUD_URL, self.loop, self.executor)
        et = parsing.parse_html(html)
        els = et.xpath(self.ACCOUNTS_LIST_URL_XPATH)

        for el in els:
            list_ = AccountList(url=el.get('href'), label=el.getparent().get('aria-labelledby'))
            lists.append(list_)

        return lists

    async def get_accounts(self, accounts_lists: List[AccountList]) -> List[NotableAccount]:
        logger.info("Parsing notable accounts from lists...", extra={'count': len(accounts_lists)})

        coros = list()

        for accounts_list in accounts_lists:
            coro = self._get_raw_accounts_from_pages(accounts_list)
            coros.append(coro)

        accounts_raw: Tuple[List[RawNotableAccount], ...] = await asyncio.gather(*coros)
        accounts_raw_reduced: List[RawNotableAccount] = functools.reduce(operator.add, accounts_raw, list())
        accounts_deduped = self._dedupe_raw_accounts(accounts_raw_reduced)

        return accounts_deduped

    async def write_accounts(self, accounts: List[NotableAccount]) -> None: ...

    async def _get_raw_accounts_from_pages(self, account_list: AccountList) -> List[RawNotableAccount]:
        logger.info(
            "Parsing notable accounts from list...",
            extra={"url": account_list.url, "label": account_list.label},
        )

        raw_accounts: List[RawNotableAccount] = list()

        page_number = self.FIRST_PAGE_NUMBER
        page_raw_accounts = await self._get_raw_accounts_from_page(account_list, page_number)

        while page_raw_accounts:
            raw_accounts = raw_accounts + page_raw_accounts

            page_number += 1
            page_raw_accounts = await self._get_raw_accounts_from_page(account_list, page_number)

        return raw_accounts

    async def _get_raw_accounts_from_page(self, account_list: AccountList, page_number: int) -> List[RawNotableAccount]:
        raw_accounts = list()

        url = f'{settings.ES_BASE_URL}{account_list.url}/{page_number}'
        html = await http.fetch_or_return_none(url, self.loop, self.executor)

        if html is None:
            logger.info('Cannot fetch URL, skipping page', extra={'url': account_list.url, 'page_number': page_number})
            return list()

        et = parsing.parse_html(html)
        els = et.xpath(self.ACCOUNT_ROW_XPATH)

        logger.info(
            'Parsed account rows',
            extra={'count': len(els), 'url': account_list.url, 'page_number': page_number},
        )

        for el in els:
            address_els = el.xpath(parsing.css_to_xpath('td:nth-child(1)'))
            name_els = el.xpath(parsing.css_to_xpath('td:nth-child(2)'))

            if not address_els or not name_els:
                logger.info(
                    'Cannot parse row, skipping',
                    extra={
                        'url': account_list.url,
                        'page_number': page_number,
                        'address_els': address_els,
                        'name_els': name_els,
                    }
                )
                continue

            raw_accounts.append(
                RawNotableAccount(
                    address=parsing.get_cleaned_text(address_els[0]),
                    name=parsing.get_cleaned_text(name_els[0]),
                    label=account_list.label,
                )
            )

        return raw_accounts

    def _dedupe_raw_accounts(self, raw_accounts: List[RawNotableAccount]) -> List[NotableAccount]:
        """
        One account can appears in multiple `AccountList`s with the same data
        but different labels.
        """
        accounts_labels: DefaultDict[str, Set[str]] = collections.defaultdict(set)
        accounts_deduped: Dict[str, NotableAccount] = dict()

        for raw_account in raw_accounts:
            accounts_labels[raw_account.address].add(raw_account.label)

        for raw_account in raw_accounts:
            if raw_account.address in accounts_deduped:
                continue

            accounts_deduped[raw_account.address] = NotableAccount(
                address=raw_account.address,
                name=raw_account.name,
                labels=tuple(sorted(accounts_labels[raw_account.address])),
            )

        return list(accounts_deduped.values())
