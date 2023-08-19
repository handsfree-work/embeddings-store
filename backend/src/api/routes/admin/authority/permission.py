import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.api.dependencies.repository import get_repository
from src.modules.account.models.db.permission import PermissionEntity
from src.modules.account.repository.permission import PermissionRepository
from src.modules.base.models.schemas.response import RestfulRes, ListRes, PageQuery, PageRes
from src.repository.crud import SelectOptions
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/authority/permission", tags=["admin.authority.permission"])


@router.post(
    path="/page",
    name="authority:permission:page",
    dependencies=[Depends(PermissionChecker(per="authority:permission:view"))],
    response_model=RestfulRes[ListRes[PermissionEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def permission_page(
        page: PageQuery[PermissionEntity],
        permission_repo: PermissionRepository = Depends(get_repository(repo_type=PermissionRepository)),

) -> RestfulRes[PageRes[PermissionEntity]]:
    page_res = await permission_repo.page(page)
    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="authority:permission:get",
    dependencies=[Depends(PermissionChecker(per="authority:permission:view"))],
    response_model=RestfulRes[PermissionEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def permission_get(
        id: int,
        permission_repo: PermissionRepository = Depends(get_repository(repo_type=PermissionRepository)),
) -> RestfulRes[PermissionEntity]:
    permission = await permission_repo.get(id=id, options=SelectOptions())
    return RestfulRes.success(data=permission)


@router.post(
    path="/tree",
    name="authority:permission:tree",
    dependencies=[Depends(PermissionChecker(per="authority:permission:view"))],
    response_model=RestfulRes[ListRes[PermissionEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def permission_tree(
        permission_repo: PermissionRepository = Depends(get_repository(repo_type=PermissionRepository)),
) -> RestfulRes[ListRes[PermissionEntity]]:
    tree = await permission_repo.tree()
    return RestfulRes.success_list(data=tree)


@router.post(
    path="/add",
    name="authority:permission:add",
    dependencies=[Depends(PermissionChecker(per="authority:permission:add"))],
    response_model=RestfulRes[PermissionEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def permission_add(
        permission: PermissionEntity,
        permission_repo: PermissionRepository = Depends(get_repository(repo_type=PermissionRepository)),
) -> RestfulRes[PermissionEntity]:
    permission = await permission_repo.create(permission)
    return RestfulRes.success(data=permission)


@router.post(
    path="/update",
    name="authority:permission:update",
    dependencies=[Depends(PermissionChecker(per="authority:permission:update"))],
    response_model=RestfulRes[PermissionEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def permission_update(
        permission: PermissionEntity,
        repository: PermissionRepository = Depends(get_repository(repo_type=PermissionRepository)),
) -> PermissionEntity:
    try:
        for_update = await repository.update(permission.id, permission)
    except EntityDoesNotExist:
        return RestfulRes.error(message="用户不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="authority:permission:delete",
             dependencies=[Depends(PermissionChecker(per="authority:permission:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def permission_delete(
        id: int,
        permission_repo: PermissionRepository = fastapi.Depends(get_repository(repo_type=PermissionRepository))
) -> RestfulRes[str]:
    await permission_repo.delete(id=id)
    return RestfulRes.success()
