import datetime
from typing import List

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import functions

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import SelectOptions
from src.repository.table import Base

from enum import Enum


class EmDocumentEntity(BaseSchemaModel):
    """
    Embedding collection entity
    """
    id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    collection_id: int | None = None
    source_id: int | None = None
    source_index: int | None = None
    title: str | None = None
    content: str | None = None
    embedding: List[float] | None = None
    embedding_half: List[float] | None = None
    score: float | None = None

    def get_embedding_content(self) -> str:
        return self.title + "\n" + self.content
