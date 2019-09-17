import logging
from asyncio import AbstractEventLoop
from typing import Generator

import alembic.config
import pytest
from aiopg.sa import Engine, create_engine
from sqlalchemy import create_engine as create_engine_sync
from sqlalchemy.engine import Engine as EngineSync

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.common.tables import TABLES

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def setup_db() -> Generator[None, None, None]:
    alembic.config.main(['upgrade', 'head'])
    yield
    alembic.config.main(['downgrade', 'base'])


@pytest.fixture(autouse=True)
def truncate_db(sa_engine_sync: EngineSync) -> Generator[None, None, None]:
    yield

    tables = ",".join([table.name for table in TABLES])

    with sa_engine_sync.connect() as conn:
        conn.execute(f"TRUNCATE {tables};")


@pytest.fixture
async def sa_engine(loop: AbstractEventLoop) -> Engine:
    return await create_engine(settings.DB_DSN)


@pytest.fixture
def sa_engine_sync() -> EngineSync:
    return create_engine_sync(settings.DB_DSN)
