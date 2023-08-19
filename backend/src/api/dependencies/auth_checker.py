import enum
from typing import Annotated, Optional

import loguru
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from src.api.dependencies.repository import get_repository
from src.modules.account.repository.role import RoleRepository
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.biz.biz_common import server_error
from src.utilities.exceptions.http.exc_401 import http_exc_401

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user = jwt_generator.retrieve_details_from_token(token)
        return user
    except ValueError as e:
        loguru.logger.error("token is invalid", e)
        raise http_exc_401(detail="token is invalid")


async def get_current_user(request: Request):
    if hasattr(request.state, 'user'):
        return request.state.user
    raise server_error(message="还未配置PermissionChecker")


class AuthType(str, enum.Enum):
    Guest: str = "guest"
    LoginOptional: str = "login_optional"
    LoginOnly: str = "login_only"


class PermissionChecker:
    def __init__(self, per: str | AuthType = None):
        self.per = per
        pass

    async def __call__(self,
                       request: Request,
                       token: str = Depends(oauth2_scheme),
                       role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository))
                       ) -> Optional[str]:
        request.state.user = None
        if self.per == AuthType.Guest or self.per == '' or self.per is None:
            return None

        # check token
        must_login = self.per != AuthType.LoginOptional

        if token is None or token == '':
            if must_login:
                raise  http_exc_401(detail="token is invalid")

        try:
            user = jwt_generator.retrieve_details_from_token(token)
            request.state.user = user
        except Exception as e:
            if must_login:
                raise e

        if self.per == AuthType.LoginOnly or self.per == AuthType.LoginOptional:
            return None
        # check permission
        passed = await role_repo.check_permission(request.state.user.roles, self.per)
        if not passed:
            raise  http_exc_401(detail="权限不足")
