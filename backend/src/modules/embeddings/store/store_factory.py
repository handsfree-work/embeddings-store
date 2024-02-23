from typing import List

from src.config.config import settings
from src.modules.base.models.schemas.response import PageQuery, PageRes
from src.modules.embeddings.models.db.em_document import EmDocumentEntity


class AbstractVectorStore:

    async def init(self):
        raise NotImplementedError()

    async def store(self, documents: list):
        raise NotImplementedError()

    async def search(self, query: List[float], top_k: int = 10, condition: EmDocumentEntity = None,
                     half: bool = False) -> list:
        raise NotImplementedError()

    async def page(self, page_query: PageQuery[EmDocumentEntity]) -> PageRes[EmDocumentEntity]:
        raise NotImplementedError()


class VectorStoreFactory:
    def __init__(self):
        self.vector_store_map = {}

    async def get_vector_store(self) -> AbstractVectorStore:
        vector_store_type = settings.vector_store.type
        if vector_store_type == "pgvector":
            if "pgvector" not in self.vector_store_map:
                from src.modules.embeddings.store.pgvector.pgvector_store import PgvectorStore
                pgvector_ = PgvectorStore()
                self.vector_store_map["pgvector"] = pgvector_
            pgvector_ = self.vector_store_map["pgvector"]
            await pgvector_.init()
            return pgvector_
        else:
            raise ValueError(f"Unknown store_type:{vector_store_type}")


vector_store_factory = VectorStoreFactory()
