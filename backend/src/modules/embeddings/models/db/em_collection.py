import datetime

import sqlalchemy
from sqlalchemy.orm import mapped_column as mapped_column, Mapped
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
    # provider: str | None = "openai"
    title: str | None = None
    key: str | None = None
    status: str | None = None


class EmCollection(Base):
    __tablename__ = "em_collection"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    key: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False, unique=True)
    # provider: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True, unique=False)
    title: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False,unique=False)
    status: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True, unique=False)

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> EmCollectionEntity:
        return EmCollectionEntity(**self.__dict__)
