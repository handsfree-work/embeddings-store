import datetime

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from src.config.manager import settings
from src.modules.account.models.db.user import User, UserEntity
from src.modules.base.models.schemas.jwt import JWTAccount, JWToken
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_401 import http_exc_401


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
            self,
            *,
            jwt_data: dict[str, str],
            expires_delta: datetime.timedelta | None = None,
    ) -> str:
        to_encode = jwt_data.copy()

        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta

        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.jwt_min)

        to_encode.update(JWToken(exp=expire, sub=settings.jwt_subject).dict())

        return jose_jwt.encode(to_encode, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def generate_access_token(self, account: UserEntity) -> str:
        if not account:
            raise EntityDoesNotExist(f"Cannot generate JWT token for without Account entity!")

        role_ids = account.roles if account.roles else []
        jwt_account = JWTAccount(id=account.id, username=account.username, email=account.email, roles=role_ids)
        return self._generate_jwt_token(
            jwt_data=jwt_account.model_dump(),
            # type: ignore
            expires_delta=datetime.timedelta(seconds=settings.jwt_access_token_expiration_time),
        )

    def retrieve_details_from_token(self, token: str, secret_key: str = settings.jwt_secret_key) -> JWTAccount:
        try:
            payload = jose_jwt.decode(token=token, key=secret_key, algorithms=[settings.jwt_algorithm])
            jwt_account = JWTAccount(**payload)

        except JoseJWTError as token_decode_error:
            raise http_exc_401(detail="Could not validate credentials")

        except pydantic.ValidationError as validation_error:
            raise http_exc_401("Invalid payload in token")

        return jwt_account


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
