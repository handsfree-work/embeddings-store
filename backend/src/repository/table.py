import typing

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class DBTable(AsyncAttrs, DeclarativeBase):
    metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()  # type: ignore


Base: typing.Type[DeclarativeBase] = DBTable
