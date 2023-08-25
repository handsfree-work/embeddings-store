from src.modules.embeddings.models.db.em_collection import EmCollection, EmCollectionEntity
from src.repository.crud import BaseCRUDRepository


class CollectionRepository(BaseCRUDRepository[EmCollection, EmCollectionEntity]):
    model = EmCollection
    pass
