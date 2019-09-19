from aiohttp import web

from jibrel_notable_accounts.common.types import AiohttpHandler


@web.middleware
async def cors_middleware(request: web.Request, handler: AiohttpHandler) -> web.Response:
    response = await handler(request)

    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Request-Method'] = 'POST, GET, OPTIONS, HEAD'

    return response
