from src.modules.embeddings.models.db.em_document import EmDocumentEntity
from src.modules.embeddings.store.pgvector.model import Document
from src.repository.crud import BaseCRUDRepository


class DocumentStoreRepository(BaseCRUDRepository[Document, EmDocumentEntity]):
    model = Document
    pass
