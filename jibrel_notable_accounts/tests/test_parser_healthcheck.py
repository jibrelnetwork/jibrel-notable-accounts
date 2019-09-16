import pytest

from aiohttp.test_utils import TestClient
from aiopg.sa import SAConnection
from pytest_mock import MockFixture
from sqlalchemy.exc import DatabaseError


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_healthcheck_everything_is_ok(parser_cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})

    result = await parser_cli.get('/healthcheck', json=dict())

    assert result.status == 200
    assert await result.json() == {
        "healthy": True,
        "isProxyHealthy": True,
        "isDbHealthy": True,
        "isLoopHealthy": True,
    }


@pytest.mark.usefixtures('setup_faulty_proxies')
async def test_healthcheck_proxy_is_bad(parser_cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})

    result = await parser_cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": False,
        "isDbHealthy": True,
        "isLoopHealthy": True,
    }


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_healthcheck_db_is_bad(parser_cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})
    mocker.patch.object(SAConnection, 'execute', side_effect=DatabaseError)

    result = await parser_cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": True,
        "isDbHealthy": False,
        "isLoopHealthy": True,
    }


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_healthcheck_loop_is_bad(parser_cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(10000)})

    result = await parser_cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": True,
        "isDbHealthy": True,
        "isLoopHealthy": False,
    }


@pytest.mark.usefixtures('setup_faulty_proxies')
async def test_healthcheck_everything_is_bad(parser_cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(10000)})
    mocker.patch.object(SAConnection, 'execute', side_effect=DatabaseError)

    result = await parser_cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": False,
        "isDbHealthy": False,
        "isLoopHealthy": False,
    }
