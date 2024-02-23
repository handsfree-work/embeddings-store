import datetime

import sqlalchemy
from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, Text
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import functions

from src.modules.embeddings.models.db.em_document import EmDocumentEntity
from src.modules.embeddings.store.pgvector.table import Base
from src.repository.schema import SelectOptions


class Document(Base):
    __tablename__ = 'document'

    id = mapped_column(Integer, primary_key=True)
    collection_id = mapped_column(Integer)
    source_id = mapped_column(Integer)
    source_index = mapped_column(Integer)
    title = mapped_column(Text)
    content = mapped_column(Text)
    embedding = mapped_column(Vector(1536))
    embedding_half = mapped_column(Vector(768))
    created_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=functions.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    def to_entity(self, options: SelectOptions = None):
        return EmDocumentEntity(**self.__dict__)
