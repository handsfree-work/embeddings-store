import datetime

import pydantic


class JWToken(pydantic.BaseModel):
    exp: datetime.datetime
    sub: str


class JWTAccount(pydantic.BaseModel):
    id: int
    username: str
    email: pydantic.EmailStr | None = None
    roles: list[int] = []
