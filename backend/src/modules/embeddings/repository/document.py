from src.config.config import settings
from src.modules.ai.service.local_ai_client import LocalAIClient
from src.modules.ai.service.openai_client import OpenAiClient, EmbeddingRequest, model_registry
from src.modules.base.models.schemas.response import PageQuery, PageRes
from src.modules.embeddings.models.db.em_document import EmDocumentEntity
from src.modules.embeddings.store.store_factory import vector_store_factory


class DocumentRepository():
    def __init__(self):
        self.openai = OpenAiClient(model=model_registry.text_embedding_ada_002)
        self.localAi = LocalAIClient(setting=settings.localAi)

    def is_local(self):
        if settings.embedding.provider == 'local':
            return True
        return False
    async def embedding(self, req: EmbeddingRequest):
        if self.is_local():
            return await self.localAi.embedding(req)
        else:
            return await self.openai.embedding(req)

    async def page(self, page_query: PageQuery[EmDocumentEntity]) -> PageRes[EmDocumentEntity]:
        store = await vector_store_factory.get_vector_store()
        return await store.page(page_query)
        pass

    async def create(self, document: EmDocumentEntity):
        embedding = await self.embedding(req=EmbeddingRequest(input=document.get_embedding_content()))
        if self.is_local():
            document.embedding_half = embedding
        else:
            document.embedding = embedding

        store = await vector_store_factory.get_vector_store()
        return await store.create(document)
        pass

    async def search(self, query: str, top_k: int = 10, condition: EmDocumentEntity = None) -> list[EmDocumentEntity]:
        store = await vector_store_factory.get_vector_store()
        query_embedding = await self.embedding(req=EmbeddingRequest(input=query))

        return await store.search(query_embedding, top_k, condition,half=self.is_local())
        pass

    async def update(self, document: EmDocumentEntity):
        embedding = await self.embedding(req=EmbeddingRequest(input=document.get_embedding_content()))
        if self.is_local():
            document.embedding_half = embedding
        else:
            document.embedding = embedding
        store = await vector_store_factory.get_vector_store()
        return await store.update(document)
        pass

    async def delete(self, id: int):
        store = await vector_store_factory.get_vector_store()
        return await store.delete(id)
        pass

    async def delete_by_source_id(self, source_id: int):
        store = await vector_store_factory.get_vector_store()
        return await store.delete_by_source_id(source_id)
        pass

    async def delete_by_collection_id(self, collection_id: int):
        store = await vector_store_factory.get_vector_store()
        return await store.delete_by_collection_id(collection_id)
        pass
