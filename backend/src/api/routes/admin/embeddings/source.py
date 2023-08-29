import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.api.dependencies.repository import get_repository
from src.modules.base.models.schemas.response import RestfulRes, PageQuery, PageRes
from src.modules.embeddings.models.db.em_source import EmSourceEntity
from src.modules.embeddings.repository.source import SourceRepository
from src.repository.crud import SelectOptions
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/embeddings/source", tags=["admin.embeddings.source"])


@router.post(
    path="/page",
    name="embeddings:source:page",
    dependencies=[Depends(PermissionChecker(per="embeddings:source:view"))],
    response_model=RestfulRes[PageRes[EmSourceEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def source_page(
        page: PageQuery[EmSourceEntity],
        repo: SourceRepository = Depends(get_repository(repo_type=SourceRepository)),
) -> RestfulRes[PageRes[EmSourceEntity]]:
    page_res = await repo.page(page, options=SelectOptions())
    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="embeddings:source:get",
    dependencies=[Depends(PermissionChecker(per="embeddings:source:view"))],
    response_model=RestfulRes[EmSourceEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def source_get(
        id: int,
        repo: SourceRepository = Depends(get_repository(repo_type=SourceRepository)),
) -> RestfulRes[EmSourceEntity]:
    source = await repo.get(id=id)
    return RestfulRes.success(data=source)


@router.post(
    path="/add",
    name="embeddings:source:add",
    dependencies=[Depends(PermissionChecker(per="embeddings:source:add"))],
    response_model=RestfulRes[EmSourceEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def source_add(
        source: EmSourceEntity,
        repo: SourceRepository = Depends(get_repository(repo_type=SourceRepository)),
) -> RestfulRes[EmSourceEntity]:
    source = await repo.create(source)
    return RestfulRes.success(data=source)


@router.post(
    path="/update",
    name="embeddings:source:update",
    dependencies=[Depends(PermissionChecker(per="embeddings:source:update"))],
    response_model=RestfulRes[EmSourceEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def source_update(
        source: EmSourceEntity,
        repo: SourceRepository = Depends(get_repository(repo_type=SourceRepository)),
) -> EmSourceEntity:
    try:
        for_update = await repo.update(source.id, source)
    except EntityDoesNotExist:
        return RestfulRes.error(message="source不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="embeddings:source:delete",
             dependencies=[Depends(PermissionChecker(per="account:source:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def source_delete(
        id: int,
        repo: SourceRepository = fastapi.Depends(get_repository(repo_type=SourceRepository))
) -> RestfulRes[str]:
    await repo.delete(id=id)
    return RestfulRes.success()


@router.post(path="/upload",
             name="embeddings:source:view",
             dependencies=[Depends(PermissionChecker(per="account:source:view"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def source_delete(
        id: int,
        repo: SourceRepository = fastapi.Depends(get_repository(repo_type=SourceRepository))
) -> RestfulRes[str]:
    await repo.delete(id=id)
    return RestfulRes.success()


@router.post(path="/import",
             name="embeddings:source:import",
             dependencies=[Depends(PermissionChecker(per="account:source:import"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def source_import(
        id: int,
        repo: SourceRepository = fastapi.Depends(get_repository(repo_type=SourceRepository))
) -> RestfulRes[str]:
    await repo.do_import(id)
    return RestfulRes.success()