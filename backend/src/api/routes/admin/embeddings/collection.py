import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.api.dependencies.repository import get_repository
from src.modules.base.models.schemas.response import RestfulRes, PageQuery, PageRes, ListRes
from src.modules.embeddings.models.db.em_collection import EmCollectionEntity
from src.modules.embeddings.repository.collection import CollectionRepository
from src.repository.crud import SelectOptions
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/embeddings/collection", tags=["admin.embeddings.collection"])


@router.post(
    path="/page",
    name="embeddings:collection:page",
    dependencies=[Depends(PermissionChecker(per="embeddings:collection:view"))],
    response_model=RestfulRes[PageRes[EmCollectionEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def collection_page(
        page: PageQuery[EmCollectionEntity],
        repo: CollectionRepository = Depends(get_repository(repo_type=CollectionRepository)),
) -> RestfulRes[PageRes[EmCollectionEntity]]:
    page_res = await repo.page(page, options=SelectOptions())
    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="embeddings:collection:get",
    dependencies=[Depends(PermissionChecker(per="embeddings:collection:view"))],
    response_model=RestfulRes[EmCollectionEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def collection_get(
        id: int,
        repo: CollectionRepository = Depends(get_repository(repo_type=CollectionRepository)),
) -> RestfulRes[EmCollectionEntity]:
    collection = await repo.get(id=id)
    return RestfulRes.success(data=collection)


@router.post(
    path="/list",
    name="embeddings:collection:list",
    dependencies=[Depends(PermissionChecker(per="embeddings:collection:view"))],
    response_model=RestfulRes[ListRes[EmCollectionEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def collection_list(
        repo: CollectionRepository = Depends(get_repository(repo_type=CollectionRepository)),
) -> RestfulRes[ListRes[EmCollectionEntity]]:
    collections = await repo.find()
    return RestfulRes.success_list(data=collections)


@router.post(
    path="/add",
    name="embeddings:collection:add",
    dependencies=[Depends(PermissionChecker(per="embeddings:collection:add"))],
    response_model=RestfulRes[EmCollectionEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def collection_add(
        collection: EmCollectionEntity,
        repo: CollectionRepository = Depends(get_repository(repo_type=CollectionRepository)),
) -> RestfulRes[EmCollectionEntity]:
    collection = await repo.create(collection)
    return RestfulRes.success(data=collection)


@router.post(
    path="/update",
    name="embeddings:collection:update",
    dependencies=[Depends(PermissionChecker(per="embeddings:collection:update"))],
    response_model=RestfulRes[EmCollectionEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def collection_update(
        collection: EmCollectionEntity,
        repo: CollectionRepository = Depends(get_repository(repo_type=CollectionRepository)),
) -> EmCollectionEntity:
    try:
        for_update = await repo.update(collection.id, collection)
    except EntityDoesNotExist:
        return RestfulRes.error(message="集合不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="embeddings:collection:delete",
             dependencies=[Depends(PermissionChecker(per="account:collection:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def collection_delete(
        id: int,
        repo: CollectionRepository = fastapi.Depends(get_repository(repo_type=CollectionRepository))
) -> RestfulRes[str]:
    await repo.delete(id=id)
    return RestfulRes.success()
