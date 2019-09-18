from typing import Optional

from sqlalchemy import select
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

    if addresses:
        select_query = select_query.where(notable_accounts_t.c.address.in_(addresses))

    return select_query
