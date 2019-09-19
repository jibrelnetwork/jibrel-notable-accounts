from aiohttp.test_utils import TestClient
from aiopg.sa import SAConnection
from pytest_mock import MockFixture
from sqlalchemy.exc import DatabaseError


async def test_healthcheck_everything_is_ok(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})

    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 200
    assert await result.json() == {
        "healthy": True,
        "isDbHealthy": True,
        "isLoopHealthy": True,
    }


async def test_healthcheck_db_is_bad(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(9999)})
    mocker.patch.object(SAConnection, 'execute', side_effect=DatabaseError)

    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isDbHealthy": False,
        "isLoopHealthy": True,
    }


async def test_healthcheck_loop_is_bad(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(10000)})

    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isDbHealthy": True,
        "isLoopHealthy": False,
    }


async def test_healthcheck_everything_is_bad(cli: TestClient, mocker: MockFixture) -> None:
    mocker.patch('asyncio.all_tasks', return_value={x for x in range(10000)})
    mocker.patch.object(SAConnection, 'execute', side_effect=DatabaseError)

    result = await cli.get('/healthcheck', json=dict())

    assert result.status == 400
    assert await result.json() == {
        "healthy": False,
        "isDbHealthy": False,
        "isLoopHealthy": False,
    }
