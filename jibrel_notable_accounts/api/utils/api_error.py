from typing import Union

from aiohttp import web

from jibrel_notable_accounts.api.types import ApiErrorMessage, ApiErrorMessages
from jibrel_notable_accounts.api.utils.response import api_error
from jibrel_notable_accounts.common.types import AiohttpHandler


class ApiError(Exception):
    def __init__(self, errors: Union[ApiErrorMessage, ApiErrorMessages], status: int = 400) -> None:
        if isinstance(errors, dict):
            errors = [errors]

        self.errors = errors
        self.status = status


@web.middleware
async def catch_api_error_middleware(request: web.Request, handler: AiohttpHandler) -> web.Response:
    try:
        response = await handler(request)
    except ApiError as e:
        return api_error(status=e.status, errors=e.errors)

    return response
