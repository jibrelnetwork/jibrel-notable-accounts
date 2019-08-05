import prometheus_client
from aiohttp import web


async def healthcheck(request: web.Request) -> web.Response:
    is_proxy_healthy = True
    is_loop_healthy = True

    healthy = all(
        (
            is_proxy_healthy,
            is_loop_healthy,
        )
    )

    data = {
        'healthy': healthy,
        'isProxyHealthy': is_proxy_healthy,
        'isLoopHealthy': is_loop_healthy,
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
