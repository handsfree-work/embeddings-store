import datetime

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class EmRecordEntity(BaseSchemaModel):
    """
    Embedding collection entity
    """
    id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    title: str | None = None
    content: str | None = None
    collection_id: int | None = None
    source_id: int | None = None
    source_index: int | None = None
    status: str | None = None
    source: str | None = None


class EmRecord(Base):
    __tablename__ = "em_record"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    collection_id: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False)
    source_id: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False)
    source_index: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False)
    title: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=False,
                                       unique=False)
    content: Mapped[str] = mapped_column(sqlalchemy.Text(), nullable=False,
                                         unique=False)
    source: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True)
    status: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True, unique=False)

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> EmRecordEntity:
        return EmRecordEntity(**self.__dict__)
