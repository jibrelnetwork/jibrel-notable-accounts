from pathlib import Path

import sys

from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, BASE_DIR)

from jibrel_notable_accounts import settings  # NOQA: E402

config = context.config
fileConfig(config.config_file_name)
target_metadata = None


def get_url():
    return settings.DB_DSN


def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
