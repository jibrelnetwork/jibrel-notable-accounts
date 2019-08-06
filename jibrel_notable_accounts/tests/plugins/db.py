import logging
from asyncio import AbstractEventLoop

import pytest
import alembic.config
from aiopg.sa import Engine, create_engine
from jibrel_notable_accounts import settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    alembic.config.main(['upgrade', 'head'])
    yield
    alembic.config.main(['downgrade', 'base'])


@pytest.mark.asyncio
@pytest.fixture
async def sa_engine(loop: AbstractEventLoop) -> Engine:
    return await create_engine(settings.DB_DSN)
