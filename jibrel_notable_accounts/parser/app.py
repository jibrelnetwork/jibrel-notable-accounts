from aiohttp import web
from jibrel_notable_accounts.monitoring import stats

from jibrel_notable_accounts.monitoring.handlers import make_healthcheck, metrics
from jibrel_notable_accounts.common.middlewares import cors_middleware
from jibrel_notable_accounts.monitoring.structs import Healthchecker


def make_app() -> web.Application:
    app = web.Application(middlewares=[cors_middleware])

    app.router.add_route('GET', '/metrics', metrics)
    app.router.add_route('GET', '/healthcheck', make_healthcheck(
        Healthchecker('isProxyHealthy', stats.is_proxy_healthy),
        Healthchecker('isLoopHealthy', stats.is_loop_healthy),
    ))

    return app
