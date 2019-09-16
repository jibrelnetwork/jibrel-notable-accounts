from typing import Any

import backoff
import mode

from aiopg import sa
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Query


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

    async def execute(self, query: Query, *params: Any) -> Any:
        async with self.engine.acquire() as connection:
            result = await connection.execute(query, params)

        return result

    async def fetch_all(self, query: Query, *params: Any) -> Any:
        async with self.engine.acquire() as connection:
            cursor = await connection.execute(query, params)
            result = await cursor.fetchall()

        return result

    async def fetch_one(self, query: Query, *params: Any) -> Any:
        async with self.engine.acquire() as connection:
            cursor = await connection.execute(query, params)
            result = await cursor.fetchone()

        return result
