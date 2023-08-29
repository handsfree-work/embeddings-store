import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.api.dependencies.repository import get_repository
from src.modules.base.models.schemas.response import RestfulRes, PageQuery, PageRes
from src.modules.embeddings.models.db.em_app import EmAppEntity
from src.modules.embeddings.repository.app import AppRepository
from src.repository.crud import SelectOptions
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/embeddings/app", tags=["admin.embeddings.app"])


@router.post(
    path="/page",
    name="embeddings:app:page",
    dependencies=[Depends(PermissionChecker(per="embeddings:app:view"))],
    response_model=RestfulRes[PageRes[EmAppEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def app_page(
        page: PageQuery[EmAppEntity],
        repo: AppRepository = Depends(get_repository(repo_type=AppRepository)),
) -> RestfulRes[PageRes[EmAppEntity]]:
    page_res = await repo.page(page, options=SelectOptions())
    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="embeddings:app:get",
    dependencies=[Depends(PermissionChecker(per="embeddings:app:view"))],
    response_model=RestfulRes[EmAppEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def app_get(
        id: int,
        repo: AppRepository = Depends(get_repository(repo_type=AppRepository)),
) -> RestfulRes[EmAppEntity]:
    app = await repo.get(id=id)
    return RestfulRes.success(data=app)


@router.post(
    path="/add",
    name="embeddings:app:add",
    dependencies=[Depends(PermissionChecker(per="embeddings:app:add"))],
    response_model=RestfulRes[EmAppEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def app_add(
        app: EmAppEntity,
        repo: AppRepository = Depends(get_repository(repo_type=AppRepository)),
) -> RestfulRes[EmAppEntity]:
    app = await repo.create(app)
    return RestfulRes.success(data=app)


@router.post(
    path="/update",
    name="embeddings:app:update",
    dependencies=[Depends(PermissionChecker(per="embeddings:app:update"))],
    response_model=RestfulRes[EmAppEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def app_update(
        app: EmAppEntity,
        repo: AppRepository = Depends(get_repository(repo_type=AppRepository)),
) -> EmAppEntity:
    try:
        app.app_key = None;
        app.app_id = None;
        for_update = await repo.update(app.id, app)
    except EntityDoesNotExist:
        return RestfulRes.error(message="app不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="embeddings:app:delete",
             dependencies=[Depends(PermissionChecker(per="account:app:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def app_delete(
        id: int,
        repo: AppRepository = fastapi.Depends(get_repository(repo_type=AppRepository))
) -> RestfulRes[str]:
    await repo.delete(id=id)
    return RestfulRes.success()
