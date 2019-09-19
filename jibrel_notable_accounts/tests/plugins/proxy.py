import itertools

import pytest
from pytest_mock import MockFixture

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.parser.utils.proxy import Proxy
from jibrel_notable_accounts.tests.plugins.types import SettingsOverrider, ProxiesSetter


@pytest.fixture()
def setup_ok_proxies(_setup_proxies: ProxiesSetter) -> None:
    _setup_proxies(False)


@pytest.fixture()
def setup_faulty_proxies(_setup_proxies: ProxiesSetter) -> None:
    _setup_proxies(True)


@pytest.fixture()
def _setup_proxies(override_settings: SettingsOverrider, mocker: MockFixture) -> ProxiesSetter:
    def _wrapper(are_faulty: bool) -> None:
        override_settings('PROXY_USER', 'user')
        override_settings('PROXY_PASS', 'pass')

        proxies = [Proxy.from_host(f'{x}.proxy.com:{x}') for x in range(len(settings.PROXY_LIST))]

        if are_faulty:
            for proxy in proxies:
                proxy.write_failure()

        proxies_cycle = itertools.cycle(proxies)

        mocker.patch('jibrel_notable_accounts.parser.utils.proxy.proxies', proxies)
        mocker.patch('jibrel_notable_accounts.parser.utils.proxy.proxies_cycle', proxies_cycle)

    return _wrapper
