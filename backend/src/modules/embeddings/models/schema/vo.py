from src.modules.base.models.schemas.base import BaseSchemaModel


class SearchRequest(BaseSchemaModel):
    collection_id: int | None = None
    query: str | None = None
    limit: int | None = None
    min_score: float | None = None
