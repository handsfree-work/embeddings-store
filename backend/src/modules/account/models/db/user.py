import datetime
from typing import List

import pydantic
import sqlalchemy
from sqlalchemy.orm import mapped_column as mapped_column, Mapped
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.account.models.db.role import RoleEntity
from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base


class UserEntity(BaseSchemaModel):
    id: int | None = None
    username: str | None = None
    nickname: str | None = None
    email: pydantic.EmailStr | None = None
    user_type: int | None = None
    is_verified: bool | None = None
    is_active: bool | None = None
    is_logged_in: bool | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    roles: List[RoleEntity] | None = None
    role_ids: List[int] | None = None


class User(Base):  # type: ignore
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    username: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    nickname: Mapped[str] = mapped_column(
        sqlalchemy.String(length=64), nullable=True, unique=False
    )
    email: Mapped[str] = mapped_column(sqlalchemy.String(length=64), nullable=True, unique=True)
    _hashed_password: Mapped[str] = mapped_column(sqlalchemy.String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(sqlalchemy.String(length=1024), nullable=True)
    is_verified: Mapped[bool] = mapped_column(sqlalchemy.Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(sqlalchemy.Boolean, nullable=False, default=False)
    is_logged_in: Mapped[bool] = mapped_column(sqlalchemy.Boolean, nullable=False, default=False)
    user_type: Mapped[int] = mapped_column(sqlalchemy.INT, nullable=False, default=2)
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    __mapper_args__ = {"eager_defaults": True}

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password

    @property
    def hash_salt(self) -> str:
        return self._hash_salt

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt

    def to_entity(self, options: SelectOptions = SelectOptions()) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            nickname=self.nickname,
            user_type=self.user_type,
            email=self.email,
            is_verified=self.is_verified,
            is_active=self.is_active,
            is_logged_in=self.is_logged_in,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
