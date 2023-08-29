import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker
from src.modules.base.models.schemas.response import RestfulRes, PageQuery, PageRes, ListRes
from src.modules.embeddings.models.db.em_document import EmDocumentEntity
from src.modules.embeddings.models.schema.vo import SearchRequest
from src.modules.embeddings.repository.document import DocumentRepository
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/admin/embeddings/document", tags=["admin.embeddings.document"])


@router.post(
    path="/page",
    name="embeddings:document:page",
    dependencies=[Depends(PermissionChecker(per="embeddings:document:view"))],
    response_model=RestfulRes[PageRes[EmDocumentEntity]],
    status_code=fastapi.status.HTTP_200_OK,
)
async def document_page(
        page: PageQuery[EmDocumentEntity],
) -> RestfulRes[PageRes[EmDocumentEntity]]:
    repo = DocumentRepository()
    page_res = await repo.page(page)
    return RestfulRes.success(data=page_res)


@router.post(
    path="/get",
    name="embeddings:document:get",
    dependencies=[Depends(PermissionChecker(per="embeddings:document:view"))],
    response_model=RestfulRes[EmDocumentEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def document_get(
        id: int,
) -> RestfulRes[EmDocumentEntity]:
    repo = DocumentRepository()
    document = await repo.get(id=id)
    return RestfulRes.success(data=document)


@router.post(
    path="/add",
    name="embeddings:document:add",
    dependencies=[Depends(PermissionChecker(per="embeddings:document:add"))],
    response_model=RestfulRes[EmDocumentEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def document_add(
        document: EmDocumentEntity,
) -> RestfulRes[EmDocumentEntity]:
    repo = DocumentRepository()
    document = await repo.create(document)
    return RestfulRes.success(data=document)


@router.post(
    path="/update",
    name="embeddings:document:update",
    dependencies=[Depends(PermissionChecker(per="embeddings:document:update"))],
    response_model=RestfulRes[EmDocumentEntity],
    status_code=fastapi.status.HTTP_200_OK,
)
async def document_update(
        document: EmDocumentEntity,
) -> EmDocumentEntity:
    repo = DocumentRepository()
    try:
        for_update = await repo.update(document)
    except EntityDoesNotExist:
        return RestfulRes.error(message="document不存在")

    return RestfulRes.success(data=for_update)


@router.post(path="/delete",
             name="embeddings:document:delete",
             dependencies=[Depends(PermissionChecker(per="embeddings:document:delete"))],
             response_model=RestfulRes[str],
             status_code=fastapi.status.HTTP_200_OK)
async def document_delete(
        id: int,
) -> RestfulRes[str]:
    repo = DocumentRepository()
    await repo.delete(id=id)
    return RestfulRes.success()


@router.post(path="/search",
             name="embeddings:document:view",
             dependencies=[Depends(PermissionChecker(per="embeddings:document:view"))],
             response_model=RestfulRes[ListRes[EmDocumentEntity]],
             status_code=fastapi.status.HTTP_200_OK)
async def document_search(
        body: SearchRequest,
) -> RestfulRes[ListRes[EmDocumentEntity]]:
    repo = DocumentRepository()
    condition = EmDocumentEntity(collection_id=body.collection_id)
    res = await repo.search(body.query, body.limit, condition)
    return RestfulRes.success_list(data=res)
