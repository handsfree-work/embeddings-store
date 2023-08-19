import datetime
from typing import List

import pydantic
import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column, Mapped, relationship
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class EmCollectionEntity(BaseSchemaModel):
    """
    Embedding collection entity
    """
    id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    title: str | None = None
    name: str | None = None
    status: str | None = None


class EmCollection(Base):
    __tablename__ = "em_collection"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=False, unique=True)
    title: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=False,
                                                            unique=False)
    status: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=True, unique=False)

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> EmCollectionEntity:
        return EmCollectionEntity(**self.__dict__)
