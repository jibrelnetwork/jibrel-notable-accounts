import pytest

from aiohttp.test_utils import TestClient
from pytest_mock import MockFixture


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_healthcheck_everything_is_ok(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})
    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 200
    assert await result.json() == {
        "healthy": True,
        "isProxyHealthy": True,
        "isLoopHealthy": True,
    }


@pytest.mark.usefixtures('setup_faulty_proxies')
async def test_healthcheck_proxy_is_bad(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})
    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": False,
        "isLoopHealthy": True,
    }


@pytest.mark.usefixtures('setup_ok_proxies')
async def test_healthcheck_loop_is_bad(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(10000)})

    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": True,
        "isLoopHealthy": False,
    }


@pytest.mark.usefixtures('setup_faulty_proxies')
async def test_healthcheck_everything_is_bad(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(10000)})

    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isProxyHealthy": False,
        "isLoopHealthy": False,
    }
