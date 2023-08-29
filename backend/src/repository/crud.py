from typing import Generic, TypeVar

import typing

import loguru
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import func, column
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload, joinedload
from sqlalchemy.sql import functions

from src.modules.base.models.schemas.response import PageRes, PageQuery
from src.repository.schema import SelectOptions
from src.utilities.exceptions.biz.biz_common import client_error
from src.utilities.exceptions.database import EntityDoesNotExist

T = TypeVar('T')
E = TypeVar('E')


class SessionWrapper:
    def __init__(self, session: SQLAlchemyAsyncSession = None):
        self.session: SQLAlchemyAsyncSession = session
        self.after_commit_callbacks: list[typing.Callable[..., typing.Coroutine]] = list()

    def register_after_commit(self, callback: typing.Callable[..., typing.Coroutine]):
        self.after_commit_callbacks.append(callback)

    def get_after_commit_callbacks(self):
        return self.after_commit_callbacks


class BaseRepository:
    def __init__(self, session_wrapper: SessionWrapper):
        self.session_wrapper = session_wrapper

    def get_session(self) -> SQLAlchemyAsyncSession:
        return self.session_wrapper.session


class BaseCRUDRepository(BaseRepository, Generic[T, E]):
    model: T

    async def _do_query(self, stmt, options: SelectOptions = None) -> any:
        if options:
            if len(options.wheres) > 0:
                for item in options.wheres:
                    stmt = stmt.where(item)
            if options.selectinload and len(options.selectinload) > 0:
                for item in options.selectinload:
                    stmt = stmt.options(selectinload(item))
            if options.joinedload and len(options.joinedload) > 0:
                for item in options.joinedload:
                    stmt = stmt.options(joinedload(item, innerjoin=False))
            if options.order_by and len(options.order_by) > 0:
                for item in options.order_by:
                    if item.desc:
                        stmt = stmt.order_by(column(item.name).desc())
                    else:
                        stmt = stmt.order_by(column(item.name).asc())
            if options.limit > 0:
                stmt = stmt.limit(options.limit)
            if options.offset > 0:
                stmt = stmt.offset(options.offset)
            if options.query is not None:
                stmt = options.query(stmt)
        query = await self.get_session().execute(statement=stmt)
        return query

    def _entity_to_mapped_values(self, entity: E) -> dict:
        mapped_values: dict = {}
        for item in self.model.__dict__.items():
            field_name = item[0]
            field_type = item[1]
            is_column = isinstance(field_type, InstrumentedAttribute)
            if is_column:
                if hasattr(entity, field_name):
                    value = getattr(entity, field_name)
                    if value is not None:
                        mapped_values[field_name] = value
        return mapped_values

    def _where_by_entity(self, stmt, entity: E):
        mapped_values: dict = self._entity_to_mapped_values(entity)
        # 遍历
        for item in mapped_values.items():
            field_name = item[0]
            field_value = item[1]
            stmt = stmt.where(column(field_name) == field_value)
        return stmt

    def __init_subclass__(cls, **kwargs):
        for name, value in cls.__annotations__.items():
            setattr(cls, name, value)

    async def create(self, entity: E) -> E:
        try:
            create_bean = self.model(**entity.model_dump(exclude_none=True))
            self.get_session().add(instance=create_bean)
            await self.get_session().flush()
            loguru.logger.debug(f"create_bean success ,id=:{create_bean.id}")
            # await self.get_session().refresh(instance=create_bean)
            entity.id = create_bean.id
            return create_bean.to_entity()
        except sqlalchemy.exc.IntegrityError as e:
            raise client_error(message=e.orig.args[0])

    async def page(self, page_query: PageQuery[E], options: SelectOptions = None) -> PageRes[E]:
        if options is None:
            options = SelectOptions()
        # 查询list
        stmt = sqlalchemy.select(self.model)
        if page_query.query:
            stmt = self._where_by_entity(stmt, page_query.query)
        stmt = stmt.offset(page_query.pager.offset).limit(page_query.pager.limit)
        if page_query.order_by:
            for item in page_query.order_by:
                if item.desc:
                    stmt = stmt.order_by(column(item.name).desc())
                else:
                    stmt = stmt.order_by(column(item.name).asc())

        query = await self._do_query(stmt, options)
        res: typing.Sequence[T] = query.unique().scalars().all()
        entities = list()
        for item in res:
            entities.append(item.to_entity(options))

        # 查询total
        options.clear_by_count()
        stmt = sqlalchemy.select(func.count()).select_from(self.model)
        if page_query.query:
            stmt = self._where_by_entity(stmt, page_query.query)
        query = await self._do_query(stmt, options)
        total = query.scalar()
        page_query.pager.total = total
        return PageRes[E](pager=page_query.pager, order_by=page_query.order_by, list=entities)

    async def find(self, condition: E = None, options: SelectOptions = None) -> list[E]:
        stmt = sqlalchemy.select(self.model)
        if condition:
            stmt = self._where_by_entity(stmt, condition)
        query = await self._do_query(stmt, options)
        res: typing.Sequence[T] = query.scalars().all()
        entities = list()
        for item in res:
            entities.append(item.to_entity(options))
        return entities

    async def get(self, id: int, options: SelectOptions = None) -> E | None:
        stmt = sqlalchemy.select(self.model).where(self.model.id == id)
        query = await self._do_query(stmt, options)

        if not query:
            return None

        bean: T = query.scalar()
        if bean is None:
            return None
        return bean.to_entity(options)

    async def get_by_ids(self, ids: list[int], options: SelectOptions = None) -> E | None:
        stmt = sqlalchemy.select(self.model).where(self.model.id.in_(ids))
        query = await self._do_query(stmt, options)
        if not query:
            return None
        bean: T = query.scalar()
        return bean.to_entity(options)

    async def update(self, id: int, entity: any) -> E:

        select_stmt = sqlalchemy.select(self.model).where(self.model.id == id)
        query = await self.get_session().execute(statement=select_stmt)
        for_update = query.scalar()

        if not for_update:
            raise EntityDoesNotExist(f"update with id `{id}` does not exist!")  # type: ignore

        mapped_values = self._entity_to_mapped_values(entity)

        update_stmt = sqlalchemy.update(table=self.model).where(self.model.id == id).values(
            updated_at=func.now())
        update_stmt = update_stmt.values(mapped_values)

        await self.get_session().execute(statement=update_stmt)
        await self.get_session().refresh(instance=for_update)

        return for_update.to_entity()

    async def delete(self, id: int):
        stmt = sqlalchemy.delete(table=self.model).where(self.model.id == id)
        await self.get_session().execute(statement=stmt)

    async def delete_where(self, options: SelectOptions = None):
        if options is None:
            options = SelectOptions()
        stmt = sqlalchemy.delete(table=self.model)
        await self._do_query(stmt, options)
