from aiohttp.test_utils import TestClient
from aiopg.sa import Engine

from jibrel_notable_accounts.common.tables import notable_accounts_t


async def test_get_labels_returns_all_available_entries_in_db_if_addresses_are_not_specified(
        cli: TestClient,
        sa_engine: Engine,
) -> None:
    async with sa_engine.acquire() as conn:
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                'name': '0x: Token Transfer Proxy',
                'labels': ['0x Ecosystem'],
            },
        ))
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
                'name': 'Binance 1',
                'labels': ['Binance', 'Exchange'],
            },
        ))

    response = await cli.get('/v1/labels')
    response_json = await response.json()

    assert response_json == {
        'status': {
            'success': True,
            'errors': [],
        },
        'data': {
            '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4': {
                'name': '0x: Token Transfer Proxy',
                'labels': ['0x Ecosystem'],
            },
            '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE': {
                'name': 'Binance 1',
                'labels': ['Binance', 'Exchange'],
            },
        }
    }


async def test_get_labels_returns_selected_entries_in_db_if_addresses_are_specified(
        cli: TestClient,
        sa_engine: Engine,
) -> None:
    async with sa_engine.acquire() as conn:
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                'name': '0x: Token Transfer Proxy',
                'labels': ['0x Ecosystem'],
            },
        ))
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
                'name': 'Binance 1',
                'labels': ['Binance', 'Exchange'],
            },
        ))
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0xfE9e8709d3215310075d67E3ed32A380CCf451C8',
                'name': 'Binance 5',
                'labels': ['Binance', 'Exchange'],
            },
        ))

    response = await cli.get(
        '/v1/labels?addresses=0x8da0d80f5007ef1e431dd2127178d224e32c2ef4,0xfE9e8709d3215310075d67E3ed32A380CCf451C8'
    )
    response_json = await response.json()

    assert response_json == {
        'status': {
            'success': True,
            'errors': [],
        },
        'data': {
            '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4': {
                'name': '0x: Token Transfer Proxy',
                'labels': ['0x Ecosystem'],
            },
            '0xfE9e8709d3215310075d67E3ed32A380CCf451C8': {
                'name': 'Binance 5',
                'labels': ['Binance', 'Exchange'],
            },
        }
    }


async def test_get_labels_returns_selected_entries_in_db_with_query_case_insensitive(
        cli: TestClient,
        sa_engine: Engine,
) -> None:
    async with sa_engine.acquire() as conn:
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be',
                'name': 'Binance 1',
                'labels': ['Binance', 'Exchange'],
            },
        ))

    response = await cli.get('/v1/labels?addresses=0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE')
    response_json = await response.json()

    assert response_json == {
        'status': {
            'success': True,
            'errors': [],
        },
        'data': {
            '0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be': {
                'name': 'Binance 1',
                'labels': ['Binance', 'Exchange'],
            },
        }
    }
