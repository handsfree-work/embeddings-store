import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.api.dependencies.repository import get_repository
from src.modules.account.models.db.user import User
from src.modules.account.models.db.user_role import UserRole
from src.modules.account.models.schemas.user import UserEntity, UserInCreate
from src.modules.account.repository.user import UserRepository
from src.modules.account.repository.user_role import UserRoleRepository
from src.modules.base.models.schemas.response import RestfulRes, PageQuery, PageRes
from src.repository.crud import SelectOptions
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/authority/user", tags=["admin.authority.user"])


@router.post(
    path="/page",
    name="authority:user:page",
    dependencies=[Depends(PermissionChecker(per="authority:user:view"))],
    response_model=RestfulRes[PageRes[UserEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def user_page(
        page: PageQuery[UserEntity],
        user_repo: UserRepository = Depends(get_repository(repo_type=UserRepository)),
        user_role_repo: UserRoleRepository = Depends(get_repository(repo_type=UserRoleRepository)),
) -> RestfulRes[PageRes[UserEntity]]:
    page_res = await user_repo.page(page, options=SelectOptions())

    user_ids = [user.id for user in page_res.list]
    user_roles = await user_role_repo.find(options=SelectOptions().with_where(UserRole.user_id.in_(user_ids)))

    user_map = {}
    for user in page_res.list:
        user_map[user.id] = user
        user.roles = []
        user.role_ids = []

    for user_role in user_roles:
        user_map[user_role.user_id].role_ids.append(user_role.role_id)

    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="authority:user:get",
    dependencies=[Depends(PermissionChecker(per="authority:user:view"))],
    response_model=RestfulRes[UserEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def user_get(
        id: int,
        user_repo: UserRepository = Depends(get_repository(repo_type=UserRepository)),
) -> RestfulRes[UserEntity]:
    user = await user_repo.get_with_role_ids(id=id)
    return RestfulRes.success(data=user)


@router.post(
    path="/add",
    name="authority:user:add",
    dependencies=[Depends(PermissionChecker(per="authority:user:add"))],
    response_model=RestfulRes[UserEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def user_add(
        user: UserInCreate,
        user_repo: UserRepository = Depends(get_repository(repo_type=UserRepository)),
) -> RestfulRes[UserEntity]:
    user = await user_repo.create_user(user)
    return RestfulRes.success(data=user)


@router.post(
    path="/update",
    name="authority:user:update",
    dependencies=[Depends(PermissionChecker(per="authority:user:update"))],
    response_model=RestfulRes[UserEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def user_update(
        user: UserEntity,
        account_repo: UserRepository = Depends(get_repository(repo_type=UserRepository)),
) -> UserEntity:
    try:
        for_update = await account_repo.update_with_roles(user.id, user)
    except EntityDoesNotExist:
        return RestfulRes.error(message="用户不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="authority:user:delete",
             dependencies=[Depends(PermissionChecker(per="account:user:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def user_delete(
        id: int,
        user_repo: UserRepository = fastapi.Depends(get_repository(repo_type=UserRepository))
) -> RestfulRes[str]:
    await user_repo.delete(id=id)
    return RestfulRes.success()
