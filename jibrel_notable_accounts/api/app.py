import functools

import sentry_sdk
from aiohttp import web
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.api.handlers import get_labels
from jibrel_notable_accounts.api.middlewares import catch_api_error_middleware
from jibrel_notable_accounts.common import logs
from jibrel_notable_accounts.common.db import DatabaseService
from jibrel_notable_accounts.common.middlewares import cors_middleware
from jibrel_notable_accounts.monitoring import stats
from jibrel_notable_accounts.monitoring.handlers import make_healthcheck, metrics
from jibrel_notable_accounts.monitoring.stats import setup_api_metrics
from jibrel_notable_accounts.monitoring.structs import Healthchecker


async def make_app() -> web.Application:
    app = web.Application(middlewares=[cors_middleware, catch_api_error_middleware])
    app['db'] = DatabaseService(dsn=settings.DB_DSN)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_route('GET', '/v1/labels', get_labels)

    app.router.add_route('GET', '/metrics', metrics)
    app.router.add_route('GET', '/healthcheck', make_healthcheck(
        Healthchecker('isDbHealthy', functools.partial(stats.is_db_healthy, db=app['db'])),
        Healthchecker('isLoopHealthy', stats.is_loop_healthy),
    ))

    logs.configure(log_level=settings.LOG_LEVEL, no_json_formatter=settings.NO_JSON_FORMATTER)
    sentry_sdk.init(settings.RAVEN_DSN, integrations=[AioHttpIntegration()])
    setup_api_metrics()

    return app


async def on_startup(app: web.Application) -> None:
    await app['db'].start()


async def on_shutdown(app: web.Application) -> None:
    await app['db'].stop()
