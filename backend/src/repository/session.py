import asyncio
import typing

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.crud import SessionWrapper
from src.repository.database import async_db
from src.utilities.exceptions.utils import exc_to_str


async def get_readonly_session_wrapper() -> typing.AsyncGenerator[SessionWrapper, None]:
    session = async_db.create_session()
    session_wrapper = SessionWrapper(session=session)
    try:
        yield session_wrapper
    finally:
        await session.close()


async def get_session_wrapper() -> typing.AsyncGenerator[SessionWrapper, None]:
    session = async_db.create_session()
    session_wrapper = SessionWrapper(session=session)
    try:
        loguru.logger.debug("get_async_session start")
        yield session_wrapper
        await session.commit()
        loguru.logger.debug("get_async_session commit")
        after = session_wrapper.get_after_commit_callbacks()
        for callback in after:
            asyncio.create_task(callback())
    except Exception as e:
        loguru.logger.error(f"get_async_session rollback:{exc_to_str(e)}")
        await session.rollback()
        raise e
    finally:
        loguru.logger.debug("get_async_session close")
        await session.close()


async def transaction(session: AsyncSession, task: typing.Callable[[SessionWrapper], typing.Awaitable]):
    """
    事务处理，需要await等待完成
    task: 事务内执行的任务
    """
    try:
        session_wrapper = SessionWrapper(session=session)
        loguru.logger.debug("get_async_session start")
        res = await task(session_wrapper)
        await session.commit()
        loguru.logger.debug("get_async_session commit")
        after = session_wrapper.get_after_commit_callbacks()
        for callback in after:
            asyncio.create_task(callback())
        return res
    except Exception as e:
        loguru.logger.error(f"get_async_session rollback:{exc_to_str(e)}")
        await session.rollback()
        raise e
    finally:
        loguru.logger.debug("get_async_session close")
        await session.close()


async def do_transaction(task: typing.Callable[[SessionWrapper], typing.Awaitable]):
    """
    事务处理，需要await等待完成
    task: 事务内执行的任务
    """
    session = async_db.create_session()
    return await transaction(session, task)


def async_transaction(*tasks: typing.Callable[[SessionWrapper], typing.Awaitable]):
    """
    异步启动事务，非阻塞，无需await等待执行完成,没有返回值
    tasks: 事务内执行的任务
    """

    async def runnable():
        for task in tasks:
            await do_transaction(task)

    asyncio.create_task(runnable())
