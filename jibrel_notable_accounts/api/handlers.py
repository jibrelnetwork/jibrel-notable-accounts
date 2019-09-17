from typing import Optional

from aiohttp import web

from jibrel_notable_accounts.api.database_queries import select_notable_accounts
from jibrel_notable_accounts.api.serializers.labels import LabelListQueryParams, Label
from jibrel_notable_accounts.api.types import Addresses
from jibrel_notable_accounts.api.utils.misc import use_kwargs
from jibrel_notable_accounts.api.utils.response import api_success


@use_kwargs(LabelListQueryParams())
async def get_labels(
        request: web.Request,
        addresses: Optional[Addresses] = None,
) -> web.Response:
    query = select_notable_accounts(addresses)
    rows = await request.app['db'].fetch_all(query)

    data_schema = Label()
    data = data_schema.dump(rows, many=True)

    return api_success(data=data)
