from src.modules.embeddings.models.db.em_source import EmSource, EmSourceEntity
from src.repository.crud import BaseCRUDRepository


class SourceRepository(BaseCRUDRepository[EmSource, EmSourceEntity]):
    model = EmSource
    pass
