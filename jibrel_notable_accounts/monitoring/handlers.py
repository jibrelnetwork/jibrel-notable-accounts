from typing import Callable, Awaitable

import prometheus_client

from aiohttp import web

from jibrel_notable_accounts.monitoring.structs import Healthchecker

AiohttpHandler = Callable[[web.Request], Awaitable[web.Response]]


def make_healthcheck(*healthcheckers: Healthchecker) -> AiohttpHandler:
    async def healthcheck(request: web.Request) -> web.Response:
        data = {}

        for healthchecker in healthcheckers:
            data[healthchecker.key] = await healthchecker.func()

        healthy = all(data.values())

        status = 200 if healthy else 400
        data['healthy'] = healthy

        return web.json_response(data=data, status=status)

    return healthcheck


async def metrics(request: web.Request) -> web.Response:
    body = prometheus_client.exposition.generate_latest().decode('utf-8')
    content_type = prometheus_client.exposition.CONTENT_TYPE_LATEST

    # WTF: `prometheus_client.exposition.CONTENT_TYPE_LATEST` is a complete
    # header with a charset provided, i.e.:
    #
    #    text/plain; version=0.0.4; charset=utf-8
    #
    # `aiohttp.web.Response` prohibits `content_type` kwarg with charsets, so
    # content type must be set as a header instead.
    return web.Response(body=body, headers={'Content-Type': content_type})
