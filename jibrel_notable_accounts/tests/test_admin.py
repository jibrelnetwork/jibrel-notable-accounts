from typing import Callable

import pytest
from sqlalchemy.orm import Query

from jibrel_notable_accounts.admin.database_queries import update_is_admin_reviewed_true, update_is_admin_reviewed_false
from jibrel_notable_accounts.api.types import Addresses
from sqlalchemy.engine import Engine

from jibrel_notable_accounts.common.tables import notable_accounts_t


@pytest.mark.parametrize(
    'func, state_before, state_after',
    (
            (update_is_admin_reviewed_true, True, True),
            (update_is_admin_reviewed_true, False, True),
            (update_is_admin_reviewed_false, True, False),
            (update_is_admin_reviewed_false, False, False),
    )
)
def test_accounts_state_changer(
        sa_engine_sync: Engine,
        func: Callable[[Addresses], Query],
        state_before: bool,
        state_after: bool,
) -> None:
    with sa_engine_sync.connect() as conn:
        conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                'name': '1',
                'labels': ['0x Ecosystem'],
                'is_admin_reviewed': state_before,
            },
        ))
        conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
                'name': '2',
                'labels': ['Binance', 'Exchange'],
                'is_admin_reviewed': state_before,
            },
        ))
        conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x4b1a99467a284cc690e3237bc69105956816f762',
                'name': '3',
                'labels': ['One', 'Two'],
                'is_admin_reviewed': state_before,
            },
        ))

    with sa_engine_sync.connect() as conn:
        conn.execute(
            func(
                [
                    '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                    '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
                ]
            )
        )

    with sa_engine_sync.connect() as conn:
        in_db = conn.execute(notable_accounts_t.select().order_by(notable_accounts_t.c.name))
        in_db = [dict(item) for item in in_db]

    assert in_db == [
            {
                'address': '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                'name': '1',
                'labels': ['0x Ecosystem'],
                'is_admin_reviewed': state_after,
            },
            {
                'address': '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
                'name': '2',
                'labels': ['Binance', 'Exchange'],
                'is_admin_reviewed': state_after,
            },
            {
                'address': '0x4b1a99467a284cc690e3237bc69105956816f762',
                'name': '3',
                'labels': ['One', 'Two'],
                'is_admin_reviewed': state_before,
            },
    ]
