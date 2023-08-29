import datetime

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base

from enum import Enum


class EmAppEntity(BaseSchemaModel):
    """
    Embedding collection entity
    """
    id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    title: str | None = None
    app_id: str | None = None
    app_key: str | None = None


class EmApp(Base):
    __tablename__ = "em_app"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    title: Mapped[str] = mapped_column(sqlalchemy.String(length=500), nullable=False)
    app_id: Mapped[str] = mapped_column(sqlalchemy.String(length=100), nullable=False, unique=True)
    app_key: Mapped[str] = mapped_column(sqlalchemy.String(length=512), nullable=False, unique=True)

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> EmAppEntity:
        return EmAppEntity(**self.__dict__)
