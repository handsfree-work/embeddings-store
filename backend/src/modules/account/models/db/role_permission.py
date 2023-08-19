import datetime

import sqlalchemy
from sqlalchemy.orm import mapped_column as mapped_column, Mapped
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class RolePermissionEntity(BaseSchemaModel):
    id: int | None = None
    role_id: int | None = None
    permission_id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class RolePermission(Base):  # type: ignore
    __tablename__ = "sys_role_permission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    role_id: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False, unique=False)
    permission_id: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False, unique=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    __mapper_args__ = {"eager_defaults": True}

    def to_entity(self, options: SelectOptions = SelectOptions()) -> RolePermissionEntity:
        return RolePermissionEntity(
            id=self.id,
            role_id=self.role_id,
            permission_id=self.permission_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
