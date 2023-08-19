import datetime
from typing import List

import loguru
import sqlalchemy
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column, Mapped, relationship
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.account.models.db.permission import Permission, PermissionEntity
from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class RoleEntity(BaseSchemaModel):
    id: int | None = None
    name: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    permissions: list[PermissionEntity] | None = None


class Role(Base):  # type: ignore
    __tablename__ = "sys_role"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> RoleEntity:
        return RoleEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
