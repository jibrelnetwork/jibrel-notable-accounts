from typing import Any

import backoff
import mode

from aiopg import sa
from sqlalchemy.exc import OperationalError


class DatabaseService(mode.Service):
    engine: sa.Engine

    def __init__(self, dsn: str, **kwargs: Any) -> None:
        self.dsn = dsn

        super().__init__(**kwargs)

    @backoff.on_exception(backoff.expo, max_tries=3, exception=OperationalError)
    async def on_start(self) -> None:
        self.engine = await sa.create_engine(self.dsn)

    async def on_stop(self) -> None:
        self.engine.close()

        await self.engine.wait_closed()
