import prometheus_client
from aiohttp import web

from jibrel_notable_accounts.monitoring import stats


async def healthcheck(request: web.Request) -> web.Response:
    proxy_is_healthy = await stats.is_proxy_healthy()
    loop_is_healthy = await stats.is_loop_healthy()

    healthy = all(
        (
            proxy_is_healthy,
            loop_is_healthy,
        )
    )

    data = {
        'healthy': healthy,
        'isProxyHealthy': proxy_is_healthy,
        'isLoopHealthy': loop_is_healthy,
    }

    status = 200 if healthy else 400
    data['healthy'] = healthy

    return web.json_response(data=data, status=status)


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
