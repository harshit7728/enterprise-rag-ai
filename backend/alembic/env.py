import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
# Use the async engine config utility instead
from sqlalchemy.ext.asyncio import async_engine_from_config  

from alembic import context
from app.core.config import settings
from app.db.base import Base
from app.db.models import User, Conversation, Message, DocumentChunk, Document

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sanitize and force the async database URL into the config context
database_url = settings.database_url
if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%"),
)

# Target metadata for autogenerate detection
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Sync context runner that physically invokes the migration operations."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Safely execute operations under the run_sync greenlet sandbox
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Safely handle the asynchronous lifecycle for the engine connection
    try:
        asyncio.run(run_migrations_online())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_migrations_online())
