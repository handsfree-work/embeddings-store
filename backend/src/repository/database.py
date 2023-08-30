import loguru
import pydantic
from sqlalchemy.ext.asyncio import (
    create_async_engine as create_sqlalchemy_async_engine, AsyncSession, async_sessionmaker, AsyncEngine,
)
from sqlalchemy.pool import Pool as SQLAlchemyPool, QueuePool as SQLAlchemyQueuePool

from src.config.manager import settings


class AsyncDatabase:
    def __init__(self):
        # self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(
        #     url=f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USENRAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}",
        # )
        self.postgres_uri = f"{settings.db_postgres_schema}://{settings.db_postgres_username}:{settings.db_postgres_password}@{settings.db_postgres_host}:{settings.db_postgres_port}/{settings.db_postgres_db}"
        loguru.logger.info("postgres_uri:{}", self.postgres_uri)
        self.async_engine: AsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.is_db_echo_log,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_pool_overflow,
            poolclass=SQLAlchemyQueuePool,
        )
        self.async_session_maker = async_sessionmaker(self.async_engine, class_=AsyncSession,
                                                      expire_on_commit=settings.is_db_expire_on_commit)
        self.pool: SQLAlchemyPool = self.async_engine.pool

    def create_session(self):
        return self.async_session_maker()

    @property
    def set_async_db_uri(self) -> str | pydantic.PostgresDsn:
        """
        Set the synchronous database driver into asynchronous version by utilizing AsyncPG:

            `postgresql://` => `postgresql+asyncpg://`
        """
        return (
            # self.postgres_uri
            self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://")
            if self.postgres_uri
            else self.postgres_uri
        )


async_db: AsyncDatabase = AsyncDatabase()
