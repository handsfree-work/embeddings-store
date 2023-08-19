from typing import Annotated, Any, List

import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker, AuthType, get_current_user
from src.api.dependencies.repository import get_repository, get_session_wrapper
from src.modules.account.models.db.permission import PermissionEntity
from src.modules.account.models.db.user import User
from src.modules.account.models.schemas.user import UserEntity
from src.modules.account.repository.user import UserRepository
from src.modules.base.models.schemas.jwt import JWTAccount
from src.modules.base.models.schemas.response import RestfulRes, ListRes
from src.repository.crud import SessionWrapper
from src.repository.schema import SelectOptions

router = fastapi.APIRouter(prefix="/user", tags=["api.user"])


@router.post(
    "/mine",
    name="user:mine",
    dependencies=[Depends(PermissionChecker(per=AuthType.LoginOnly))],
    response_model=RestfulRes[UserEntity]
)
async def mine(
        current_user: Annotated[JWTAccount, Depends(get_current_user)],
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> RestfulRes[UserEntity]:
    user_info = await user_repo.get_with_role_ids(id=current_user.id)
    return RestfulRes.success(data=user_info)


@router.post(
    "/permissions",
    name="user:permissions",
    dependencies=[Depends(PermissionChecker(per=AuthType.LoginOnly))],
    response_model=RestfulRes[ListRes[PermissionEntity]]
)
async def permissions(
        current_user: Annotated[JWTAccount, Depends(get_current_user)],
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> RestfulRes[ListRes[PermissionEntity]]:
    permission_list = await user_repo.get_permissions(user_id=current_user.id)
    return RestfulRes.success_list(data=permission_list)
