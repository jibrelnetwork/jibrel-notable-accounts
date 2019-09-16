from typing import Optional

from aiohttp import web

from jibrel_notable_accounts.api.serializers.labels import LabelListSchema
from jibrel_notable_accounts.api.types import Addresses
from jibrel_notable_accounts.api.utils.misc import use_kwargs


@use_kwargs(LabelListSchema())
async def get_labels(
        request: web.Request,
        addresses: Optional[Addresses] = None,
) -> web.Response:
    return web.json_response()
