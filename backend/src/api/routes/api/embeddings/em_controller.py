import fastapi
from fastapi import Depends

from src.api.dependencies.auth_checker import PermissionChecker, AuthType
from src.modules.base.models.schemas.response import RestfulRes, ListRes
from src.modules.embeddings.store.store_factory import vector_store_factory

router = fastapi.APIRouter(prefix="/embeddings", tags=["api.embeddings"])


@router.post(
    "/store",
    name="embeddings:store:post",
    dependencies=[Depends(PermissionChecker(per=AuthType.Guest))],
    response_model=RestfulRes[str],
)
async def store(
) -> RestfulRes[str]:
    vector_store = await vector_store_factory.get_vector_store()
    await vector_store.store(documents=["test"])
    return RestfulRes.success()


@router.post(
    "/search",
    name="embeddings:search:post",
    dependencies=[Depends(PermissionChecker(per=AuthType.Guest))],
    response_model=RestfulRes[ListRes[str]],
)
async def search(
) -> RestfulRes[ListRes[str]]:
    vector_store = await vector_store_factory.get_vector_store()
    res = await vector_store.search(query="test", top_k=10)
    return RestfulRes.success_list(data=res)
