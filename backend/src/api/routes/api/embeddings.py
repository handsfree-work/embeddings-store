import fastapi
from fastapi import Depends

from src.api.dependencies.em_token_checker import EmTokenChecker
from src.modules.base.models.schemas.response import RestfulRes, ListRes
from src.modules.embeddings.models.db.em_document import EmDocumentEntity
from src.modules.embeddings.models.schema.vo import SearchRequest
from src.modules.embeddings.repository.document import DocumentRepository

router = fastapi.APIRouter(prefix="/embeddings", tags=["api.embeddings"])


@router.post(
    "/search",
    name="embeddings:search:post",
    dependencies=[Depends(EmTokenChecker())],
    response_model=RestfulRes[ListRes[EmDocumentEntity]],
)
async def search(
        body: SearchRequest,
) -> RestfulRes[ListRes[EmDocumentEntity]]:
    repo = DocumentRepository()
    condition = EmDocumentEntity(collection_id=body.collection_id)
    res = await repo.search(body.query, body.limit, condition)
    return RestfulRes.success_list(data=res)
