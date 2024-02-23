from typing import Optional

from src.modules.base.models.schemas.base import BaseSchemaModel


class ChatMessage(BaseSchemaModel):
    role: str
    name: str | None = None
    content: Optional[str] = None
    function_call: dict | None = None


class ChatRequest(BaseSchemaModel):
    messages: list[ChatMessage]
    functions: list[dict] | None = None
    temperature: float | None = None


class EmbeddingRequest(BaseSchemaModel):
    input: str
