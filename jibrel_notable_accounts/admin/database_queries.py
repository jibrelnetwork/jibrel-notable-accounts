import functools

from sqlalchemy import update
from sqlalchemy.orm import Query

from jibrel_notable_accounts.api.types import Addresses
from jibrel_notable_accounts.common.tables import notable_accounts_t


def update_is_admin_reviewed_state(addresses: Addresses, to: bool) -> Query:
    query = update(notable_accounts_t)
    query = query.where(notable_accounts_t.c.address.in_(addresses))
    query = query.values(is_admin_reviewed=to)

    return query


update_is_admin_reviewed_true = functools.partial(update_is_admin_reviewed_state, to=True)
update_is_admin_reviewed_false = functools.partial(update_is_admin_reviewed_state, to=False)
