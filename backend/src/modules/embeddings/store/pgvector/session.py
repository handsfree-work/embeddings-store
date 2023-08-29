from contextlib import contextmanager, asynccontextmanager

import loguru
from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from src.config.config import settings


class pgvector_db():
    def __init__(self):
        async_db_uri = settings.vector_store.pg_uri
        self.async_engine: AsyncEngine = create_async_engine(
            url=async_db_uri,
            echo=settings.base.is_db_echo_log,
            pool_size=settings.base.db_pool_size,
            max_overflow=settings.base.db_pool_overflow,
            poolclass=QueuePool
        )
        # with self.async_engine.connect() as conn:
        #     conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        #     conn.commit()
        self.async_session: AsyncSession = AsyncSession(bind=self.async_engine)
        self.async_session_maker = async_sessionmaker(self.async_engine, class_=AsyncSession)


pgvector_db = pgvector_db()


# 自定义transaction装饰器
@asynccontextmanager
async def transaction():
    session = pgvector_db.async_session_maker()
    try:
        yield session
        if session.in_transaction():
            loguru.logger.debug(f"get_async_session commit")
            await session.commit()
    except Exception as e:
        if session.in_transaction():
            loguru.logger.debug(f"get_async_session rollback:{e}")
            await session.rollback()
        raise e
    finally:
        await session.close()
