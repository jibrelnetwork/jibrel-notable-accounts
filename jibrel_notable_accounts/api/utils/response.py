from typing import Any

from aiohttp import web


def api_success(data: Any) -> web.Response:
    body = {
        'status': {
            'success': True,
            'errors': [],
        },
        'data': data
    }

    return web.json_response(body)


def api_error(errors: Any, status: int) -> web.Response:
    body = {
        'status': {
            'success': False,
            'errors': errors
        },
        'data': None,
    }

    return web.json_response(body, status=status)
