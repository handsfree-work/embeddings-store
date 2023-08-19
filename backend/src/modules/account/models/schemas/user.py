import pydantic
from pydantic import Field

from src.modules.account.models.db.user import UserEntity
from src.modules.base.models.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    username: str
    email: pydantic.EmailStr = None
    password: str = None
    user_type: int = 2


class UserInUpdate(BaseSchemaModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserInLogin(BaseSchemaModel):
    username: str
    password: str
    user_type: int = 2


class AccessToken(BaseSchemaModel):
    token: str
    expires: int


class LoginToken(BaseSchemaModel):
    access_token: AccessToken
    user: UserEntity
