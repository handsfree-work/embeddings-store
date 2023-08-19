import fastapi
import loguru as loguru
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker, AuthType
from src.api.dependencies.repository import get_repository
from src.config.manager import settings
from src.modules.account.models.schemas.user import LoginToken, AccessToken
from src.modules.account.models.schemas.user import UserInCreate, UserInLogin, UserEntity
from src.modules.account.repository.user import UserRepository
from src.modules.base.models.schemas.response import RestfulRes
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.database import EntityAlreadyExists
from src.utilities.exceptions.http.exc_400 import (
    http_exc_400,
)
from src.utilities.exceptions.http.exc_401 import http_exc_401

router = fastapi.APIRouter(prefix="/auth", tags=["api.authentication"])


@router.post(
    "/register",
    name="auth:register",
    dependencies=[Depends(PermissionChecker(per=AuthType.Guest))],
    response_model=RestfulRes[UserEntity],
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def register(
        user_create: UserInCreate,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> RestfulRes[UserEntity]:
    try:
        await user_repo.is_username_taken(username=user_create.username)
        await user_repo.is_email_taken(email=user_create.email)
    except EntityAlreadyExists:
        raise http_exc_400(detail="账号或邮箱已被注册！")

    new_account = await user_repo.create_user(account_create=user_create)
    return RestfulRes.success(data=new_account)


@router.post(
    path="/login",
    name="auth:login",
    dependencies=[Depends(PermissionChecker(per=AuthType.Guest))],
    response_model=RestfulRes[LoginToken],
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def login(
        account_login: UserInLogin,
        account_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> RestfulRes[LoginToken]:
    try:
        db_account = await account_repo.read_user_by_password_authentication(account_login=account_login)
    except Exception as e:
        raise http_exc_401(detail="账号或密码错误！")

    access_token = jwt_generator.generate_access_token(account=db_account)

    return RestfulRes.success(
        data=LoginToken(
            access_token=AccessToken(
                token=access_token,
                expires=settings.jwt_access_token_expiration_time,
            ),
            user=UserEntity(
                id=db_account.id,
                username=db_account.username,
                user_type=db_account.user_type,
                email=db_account.email,
                is_verified=db_account.is_verified,
                is_active=db_account.is_active,
                is_logged_in=db_account.is_logged_in,
                created_at=db_account.created_at,
                updated_at=db_account.updated_at,
            )
        )
    )
