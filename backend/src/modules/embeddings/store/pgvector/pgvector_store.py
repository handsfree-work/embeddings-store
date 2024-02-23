from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession, )

from src.modules.base.models.schemas.response import PageQuery, PageRes
from src.modules.embeddings.models.db.em_document import EmDocumentEntity
from src.modules.embeddings.store.pgvector.document_repo import DocumentStoreRepository
from src.modules.embeddings.store.pgvector.model import Document
from src.modules.embeddings.store.pgvector.session import pgvector_db, transaction
from src.modules.embeddings.store.store_factory import AbstractVectorStore
from src.repository.crud import SessionWrapper
from src.repository.schema import SelectOptions, OrderBy


class PgvectorStore(AbstractVectorStore):
    def __init__(self):
        # 禁止非异步的东西
        pass

    def create_session(self):
        return pgvector_db.async_session_maker()

    async def init(self):
        # Base = declarative_base()
        # Base.metadata.create_all(self.async_engine)
        pass

    def create_repo(self, session: AsyncSession):
        return DocumentStoreRepository(session_wrapper=SessionWrapper(session=session))

    async def page(self, page_query: PageQuery[EmDocumentEntity]) -> PageRes[EmDocumentEntity]:

        async with transaction() as session:
            repo = self.create_repo(session=session)
            return await repo.page(page_query,
                                   options=SelectOptions().with_order_by(OrderBy(name="id", desc=True)))

    async def create(self, document: EmDocumentEntity):

        async with transaction() as session:
            repo = self.create_repo(session=session)
            await repo.create(document)

    async def update(self, document: EmDocumentEntity):
        async with transaction() as session:
            repo = self.create_repo(session=session)
            document.updated_at = None
            document.created_at = None
            await repo.update(document.id, document)

    async def delete(self, id: int):
        async with transaction() as session:
            repo = self.create_repo(session=session)
            await repo.delete(id)

    async def delete_by_source_id(self, source_id: int):
        async with transaction() as session:
            repo = self.create_repo(session=session)
            await repo.delete_where(options=SelectOptions().with_where(Document.source_id == source_id))

    async def delete_by_collection_id(self, collection_id: int):
        async with transaction() as session:
            repo = self.create_repo(session=session)
            await repo.delete_where(options=SelectOptions().with_where(Document.collection_id == collection_id))

    async def search(self, query_embedding: list[float], top_k: int = 10, condition: EmDocumentEntity = None,half:bool = False) -> list[
        EmDocumentEntity]:
        async with transaction() as session:
            if half:
                score_ = Document.embedding_half.l2_distance(query_embedding).label("score")
            else:
                score_ = Document.embedding.l2_distance(query_embedding).label("score")
            stmt = select(Document.id,
                          Document.title,
                          Document.content,
                          score_)
            if condition is not None:
                for k, v in condition.__dict__.items():
                    if v is not None:
                        stmt = stmt.filter(getattr(Document, k) == v)
            stmt = stmt.order_by(score_).limit(top_k)

            q = await session.execute(statement=stmt)
            rows = q.all()
            print(rows)
            res: list[EmDocumentEntity] = list()
            for row in rows:
                entity = EmDocumentEntity(id=row[0], title=row[1], content=row[2], score=row[3])
                res.append(entity)
            return res
