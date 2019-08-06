import logging
from typing import Generator, AsyncGenerator

import pytest
import alembic.config
from aiopg.sa import Engine, create_engine
from jibrel_notable_accounts import settings
from jibrel_notable_accounts.common.tables import TABLES

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def setup_db() -> Generator[None, None, None]:
    alembic.config.main(['upgrade', 'head'])
    yield
    alembic.config.main(['downgrade', 'base'])


@pytest.fixture(autouse=True)
async def truncate_db(sa_engine: Engine) -> AsyncGenerator[None, None]:
    yield

    tables = ",".join([table.name for table in TABLES])

    async with sa_engine.acquire() as conn:
        conn.execute(f"TRUNCATE {tables};")


@pytest.mark.asyncio
@pytest.fixture
async def sa_engine() -> Engine:
    return await create_engine(settings.DB_DSN)
