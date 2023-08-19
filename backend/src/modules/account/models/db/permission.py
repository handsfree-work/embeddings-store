import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped as Mapped, mapped_column as mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class Permission(Base):  # type: ignore
    __tablename__ = "sys_permission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    title: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=False
    )
    code: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    parent_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer(), nullable=False, unique=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()):
        return PermissionEntity(
            id=self.id,
            title=self.title,
            code=self.code,
            parent_id=self.parent_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class PermissionEntity(BaseSchemaModel):
    id: int | None = None
    title: str | None = None
    code: str | None = None
    parent_id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    children: list['PermissionEntity'] | None = None
