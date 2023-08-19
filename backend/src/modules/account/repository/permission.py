from typing import List

from src.modules.account.models.db.permission import Permission, PermissionEntity
from src.repository.crud import BaseCRUDRepository


class PermissionRepository(BaseCRUDRepository[Permission, PermissionEntity]):
    model = Permission
    pass

    async def tree(self):
        res = await self.find()
        return self.build_tree(res)

    def build_tree(self, data: List[PermissionEntity], parent_id=0):
        tree = []
        for item in data:
            if item.parent_id == parent_id:
                children = self.build_tree(data, item.id)
                if children:
                    item.children = children
                tree.append(item)
        return tree
