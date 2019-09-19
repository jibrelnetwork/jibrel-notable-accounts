from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Query

from jibrel_notable_accounts.common.tables import notable_accounts_t
from jibrel_notable_accounts.parser.structs import NotableAccount


def insert_or_update_notable_account(notable_account: NotableAccount) -> Query:
    insert_query = insert(notable_accounts_t)
    insert_query = insert_query.values(tuple(notable_account))
    insert_query = insert_query.on_conflict_do_update(
        index_elements=[
            notable_accounts_t.c.address,
        ],
        set_={
            'name': insert_query.excluded.name,
            'labels': insert_query.excluded.labels,
            'is_admin_reviewed': insert_query.excluded.is_admin_reviewed,
        },
    )

    return insert_query


def insert_or_skip_notable_account(notable_account: NotableAccount) -> Query:
    insert_query = insert(notable_accounts_t)
    insert_query = insert_query.values(tuple(notable_account))
    insert_query = insert_query.on_conflict_do_nothing(
        index_elements=[
            notable_accounts_t.c.address,
        ],
    )

    return insert_query
