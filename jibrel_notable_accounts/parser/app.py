import functools

from aiohttp import web

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.common.db import DatabaseService
from jibrel_notable_accounts.monitoring import stats

from jibrel_notable_accounts.monitoring.handlers import make_healthcheck, metrics
from jibrel_notable_accounts.common.middlewares import cors_middleware
from jibrel_notable_accounts.monitoring.structs import Healthchecker


def make_app() -> web.Application:
    app = web.Application(middlewares=[cors_middleware])
    app['db'] = DatabaseService(dsn=settings.DB_DSN)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_route('GET', '/metrics', metrics)
    app.router.add_route('GET', '/healthcheck', make_healthcheck(
        Healthchecker('isProxyHealthy', stats.is_proxy_healthy),
        Healthchecker('isDbHealthy', functools.partial(stats.is_db_healthy, db=app['db'])),
        Healthchecker('isLoopHealthy', stats.is_loop_healthy),
    ))

    return app


async def on_startup(app: web.Application) -> None:
    await app['db'].start()


async def on_shutdown(app: web.Application) -> None:
    await app['db'].stop()
