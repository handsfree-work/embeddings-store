import openai
from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, Text, insert, select
from sqlalchemy.ext.asyncio import (
    create_async_engine as create_sqlalchemy_async_engine, AsyncSession, async_sessionmaker, AsyncEngine,
)
from sqlalchemy.orm import mapped_column
from sqlalchemy.pool import QueuePool as SQLAlchemyQueuePool

from src.config.config import settings
from src.modules.ai.service.openai_client import OpenAiClient
from src.modules.embeddings.store.pgvector.table import Base
from src.modules.embeddings.store.store_factory import AbstractVectorStore
from src.repository.crud import SessionWrapper
from src.repository.session import transaction


class Document(Base):
    __tablename__ = 'document'

    id = mapped_column(Integer, primary_key=True)
    collection_id = mapped_column(Integer)
    source_id = mapped_column(Integer)
    source_index = mapped_column(Integer)
    title = mapped_column(Text)
    content = mapped_column(Text)
    embedding = mapped_column(Vector(1536))


class PgvectorStore(AbstractVectorStore):

    def __init__(self):
        async_db_uri = settings.vector_store.pg_uri
        self.async_engine: AsyncEngine = create_sqlalchemy_async_engine(
            url=async_db_uri,
            echo=settings.base.is_db_echo_log,
            pool_size=settings.base.db_pool_size,
            max_overflow=settings.base.db_pool_overflow,
            poolclass=SQLAlchemyQueuePool,
        )
        # with self.async_engine.connect() as conn:
        #     conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        #     conn.commit()
        self.async_session: AsyncSession = AsyncSession(bind=self.async_engine)
        self.async_session_maker = async_sessionmaker(self.async_engine, class_=AsyncSession)

        self.openai = OpenAiClient()

    def create_session(self):
        return self.async_session_maker()

    async def init(self):
        # Base = declarative_base()
        # Base.metadata.create_all(self.async_engine)
        pass

    async def store(self, documents: list):
        input = [
            'The dog is barking',
            'The cat is purring',
            'The bear is growling'
        ]

        embeddings = [v['embedding'] for v in
                      openai.Embedding.create(input=input, model='text-embedding-ada-002')['data']]
        documents = [dict(content=input[i], embedding=embedding) for i, embedding in enumerate(embeddings)]

        async def task(session_wrapper: SessionWrapper = None):
            session_ = session_wrapper.session
            await session_.execute(insert(Document), documents)

        await transaction(self.create_session(), task)

    async def search(self, query: str, top_k: int = 10) -> list:
        async def task(session_wrapper: SessionWrapper):
            session_ = session_wrapper.session
            doc = await session_.get(Document, 1)
            neighbors = await session_.scalars(
                select(Document).filter(Document.id != doc.id).order_by(
                    Document.embedding.max_inner_product(doc.embedding)).limit(
                    5))
            res = list()
            for neighbor in neighbors:
                print(neighbor.content)
                res.append(neighbor.content)
            return res

        return await transaction(self.create_session(), task)
