import asyncio

from aiohttp import web

from jibrel_notable_accounts.monitoring import handlers
from jibrel_notable_accounts.common.middlewares import cors_middleware


def make_app(loop: asyncio.AbstractEventLoop) -> web.Application:
    app = web.Application(loop=loop, middlewares=[cors_middleware])

    app.router.add_route('GET', '/healthcheck', handlers.healthcheck)
    app.router.add_route('GET', '/metrics', handlers.metrics)

    return app
