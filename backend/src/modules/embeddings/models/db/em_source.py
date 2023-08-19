import datetime

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class EmSourceEntity(BaseSchemaModel):
    """
    Embedding collection entity
    """
    id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    title: str | None = None
    file_type: str | None = None
    content: str | None = None
    collection_id: int | None = None
    md5: str | None = None
    status: str | None = None


class EmSource(Base):
    __tablename__ = "em_source"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    collection_id: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False)
    name: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    title: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    file_type: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False)
    content: Mapped[str] = mapped_column(sqlalchemy.Text(), nullable=False)
    status: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True)
    md5: Mapped[str] = mapped_column(sqlalchemy.String(length=256), nullable=True)

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> EmSourceEntity:
        return EmSourceEntity(**self.__dict__)
