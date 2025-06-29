from typing import Any, Callable

import mode
from aiohttp import web

AppMaker = Callable[[], web.Application]


class ApiService(mode.Service):
    def __init__(self, port: int, app_maker: AppMaker, **kwargs: Any) -> None:
        self.port = port

        super().__init__(**kwargs)

        self.app = app_maker()
        self.runner = web.AppRunner(self.app)

    async def on_start(self) -> None:
        await self.runner.setup()
        await web.TCPSite(self.runner, '0.0.0.0', self.port).start()

    async def on_stop(self) -> None:
        await self.runner.cleanup()
