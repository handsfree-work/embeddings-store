import asyncio

from alembic import context
from alembic.config import Config
from pgvector.asyncpg import register_vector
from sqlalchemy import engine_from_config, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import NullPool as SQLAlchemyNullPool

from src.config.config import settings
from src.modules.embeddings.store.pgvector.pgvector_store import Document

print(Document)
from src.modules.embeddings.store.pgvector.table import Base

print("postgres url:" + settings.vector_store.pg_uri)
alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", str(settings.vector_store.pg_migrations_dir))
alembic_cfg.set_main_option("sqlalchemy.url", str(settings.vector_store.pg_uri))
config = alembic_cfg

target_metadata = Base.metadata


# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    print("offline")
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    print("online ")
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),  # type: ignore
            prefix="sqlalchemy.",
            poolclass=SQLAlchemyNullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        await connection.commit()
        await register_vector(connection.sync_connection.connection.driver_connection)
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
