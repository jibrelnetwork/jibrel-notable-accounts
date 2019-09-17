from typing import Callable, Awaitable

from aiohttp import web

AiohttpHandler = Callable[[web.Request], Awaitable[web.Response]]
