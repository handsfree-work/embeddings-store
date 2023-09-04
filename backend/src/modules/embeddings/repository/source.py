from src.modules.embeddings.models.db.em_source import EmSource, EmSourceEntity, SourceType, ResolveType
from src.repository.crud import BaseCRUDRepository


class SourceRepository(BaseCRUDRepository[EmSource, EmSourceEntity]):
    model = EmSource
    pass

    async def do_import(self, id):
        source = await self.get(id=id)
        if source is None:
            raise ValueError(f"Source id:{id} does not exist")
        content = source.content
        if source.resolve_type == ResolveType.direct_split:
            content = content.split("\n")
        pass