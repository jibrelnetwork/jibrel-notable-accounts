import pathlib
from asyncio import AbstractEventLoop
from concurrent.futures.thread import ThreadPoolExecutor

from aiohttp.test_utils import TestClient
from click.testing import CliRunner
from prometheus_client import CollectorRegistry

from jibrel_notable_accounts import settings
from pytest_mock import MockFixture

from jibrel_notable_accounts.monitoring.app import make_app

from typing import Any, AsyncGenerator, Generator

import pytest

from jibrel_notable_accounts.parser.service import ParserService
from jibrel_notable_accounts.tests.plugins.types import AiohttpClient, SettingsOverrider, HtmlGetter


@pytest.fixture
async def parser(loop: AbstractEventLoop) -> AsyncGenerator[ParserService, None]:
    parser = ParserService(db_dsn=settings.DB_DSN, update_if_exists=False, loop=loop)

    await parser.on_start()
    await parser.database.on_start()

    yield parser

    await parser.database.on_stop()
    await parser.on_stop()


@pytest.fixture
async def parser_with_override(loop: AbstractEventLoop) -> AsyncGenerator[ParserService, None]:
    parser = ParserService(db_dsn=settings.DB_DSN, update_if_exists=True, loop=loop)

    await parser.on_start()
    await parser.database.on_start()

    yield parser

    await parser.database.on_stop()
    await parser.on_stop()


@pytest.fixture
def executor() -> Generator[ThreadPoolExecutor, None, None]:
    executor = ThreadPoolExecutor(max_workers=1)
    yield executor
    executor.shutdown()


@pytest.fixture
def cli(loop: AbstractEventLoop, aiohttp_client: AiohttpClient) -> TestClient:
    return loop.run_until_complete(aiohttp_client(make_app(loop)))


@pytest.fixture()
def override_settings(mocker: MockFixture) -> SettingsOverrider:
    def inner(name: str, value: Any) -> None:
        mocker.patch(f'jibrel_notable_accounts.settings.{name}', value)

    return inner


@pytest.fixture()
def get_html() -> HtmlGetter:
    def _wrapper(filename: str) -> str:
        path = pathlib.Path(__file__).parent.parent / 'html' / filename
        text = path.read_text()

        return text

    return _wrapper


@pytest.fixture()
def mock_sleepers(mocker: MockFixture) -> None:
    mocker.patch('asyncio.sleep')
    mocker.patch('time.sleep')


@pytest.fixture()
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(autouse=True)
def disable_metrics_setup(mocker: MockFixture) -> None:
    # Metrics setup contributes to a 'prometheus_client.registry.REGISTRY'
    # singleton. If same metric is contributed twice, `ValueError` is raised.

    mocker.patch.object(CollectorRegistry, 'register')
