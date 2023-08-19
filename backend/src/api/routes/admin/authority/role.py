from typing import List

import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.api.dependencies.repository import get_repository
from src.modules.account.models.db.role import RoleEntity
from src.modules.account.repository.role import RoleRepository
from src.modules.base.models.schemas.base import BaseSchemaModel
from src.modules.base.models.schemas.response import RestfulRes, ListRes, PageQuery, PageRes
from src.repository.crud import SelectOptions
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/authority/role", tags=["admin.authority.role"])


@router.post(
    path="/page",
    name="authority:role:page",
    dependencies=[Depends(PermissionChecker(per="authority:role:view"))],
    response_model=RestfulRes[PageRes[RoleEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_page(
        page: PageQuery[RoleEntity],
        role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),

) -> RestfulRes[PageRes[RoleEntity]]:
    page_res = await role_repo.page(page)
    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="authority:role:get",
    dependencies=[Depends(PermissionChecker(per="authority:role:view"))],
    response_model=RestfulRes[RoleEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_get(
        id: int,
        role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),
) -> RestfulRes[RoleEntity]:
    role = await role_repo.get(id=id, options=SelectOptions())
    return RestfulRes.success(data=role)


@router.post(
    path="/get_permission_ids",
    name="authority:role:get",
    dependencies=[Depends(PermissionChecker(per="authority:role:view"))],
    response_model=RestfulRes[ListRes[int]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_get_permission_ids(
        id: int,
        role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),
) -> RestfulRes[ListRes[int]]:
    permission_ids = await role_repo.get_permission_ids(id=id)
    return RestfulRes.success_list(data=permission_ids)


@router.post(
    path="/list",
    name="authority:role:list",
    dependencies=[Depends(PermissionChecker(per="authority:role:view"))],
    response_model=RestfulRes[ListRes[RoleEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_list(
        role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),
) -> RestfulRes[ListRes[RoleEntity]]:
    roles = await role_repo.find()
    return RestfulRes.success_list(data=roles)


@router.post(
    path="/add",
    name="authority:role:add",
    dependencies=[Depends(PermissionChecker(per="authority:role:add"))],
    response_model=RestfulRes[RoleEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_add(
        role: RoleEntity,
        role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),
) -> RestfulRes[RoleEntity]:
    role = await role_repo.create(role)
    return RestfulRes.success(data=role)


@router.post(
    path="/update",
    name="authority:role:update",
    dependencies=[Depends(PermissionChecker(per="authority:role:update"))],
    response_model=RestfulRes[RoleEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_update(
        role: RoleEntity,
        account_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),
) -> RoleEntity:
    try:
        for_update = await account_repo.update(role.id, role)
    except EntityDoesNotExist:
        return RestfulRes.error(message="用户不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="authority:role:delete",
             dependencies=[Depends(PermissionChecker(per="authority:role:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def role_delete(
        id: int,
        role_repo: RoleRepository = fastapi.Depends(get_repository(repo_type=RoleRepository))
) -> RestfulRes[str]:
    await role_repo.delete(id=id)
    return RestfulRes.success()


class RoleAuthzReq(BaseSchemaModel):
    role_id: int
    permission_ids: List[int]


@router.post(
    path="/authz",
    name="authority:role:authz",
    dependencies=[Depends(PermissionChecker(per="authority:role:authz"))],
    response_model=RestfulRes[str],
    status_code=fastapi.status.HTTP_200_OK,
)
async def role_authz(
        req: RoleAuthzReq,
        role_repo: RoleRepository = Depends(get_repository(repo_type=RoleRepository)),
) -> RestfulRes[str]:
    await role_repo.authz(req.role_id, req.permission_ids)
    return RestfulRes.success()
