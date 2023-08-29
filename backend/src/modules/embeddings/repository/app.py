from datetime import datetime

from cachetools import cached, TTLCache

from src.modules.embeddings.models.db.em_app import EmApp, EmAppEntity
from src.repository.crud import BaseCRUDRepository
from src.utilities.strings.strings import random_number_string, md5


class AppRepository(BaseCRUDRepository[EmApp, EmAppEntity]):
    model = EmApp
    pass

    async def create(self, entity: EmAppEntity) -> EmAppEntity:
        datetime.now().timestamp()
        entity.app_id = str(int(datetime.now().timestamp())) + random_number_string(4)
        entity.app_key = "em_" + md5(random_number_string(10))
        return await super().create(entity)

    # 缓存单位秒
    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def check_token(self, token: str):
        beans = await self.find(condition=EmAppEntity(app_key=token))
        bean = beans[0] if len(beans) > 0 else None
        if bean is None:
            return False
        return True
