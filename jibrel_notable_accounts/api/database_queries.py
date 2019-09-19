from typing import Optional

from sqlalchemy import select, func, true
from sqlalchemy.orm import Query

from jibrel_notable_accounts.api.types import Addresses
from jibrel_notable_accounts.common.tables import notable_accounts_t

columns = [
    notable_accounts_t.c.address,
    notable_accounts_t.c.name,
    notable_accounts_t.c.labels,
]


def select_notable_accounts(addresses: Optional[Addresses]) -> Query:
    select_query = select(columns)
    select_query = select_query.where(notable_accounts_t.c.is_admin_reviewed == true())

    if addresses:
        addresses_lower = [address.lower() for address in addresses]
        select_query = select_query.where(func.lower(notable_accounts_t.c.address).in_(addresses_lower))

    return select_query
