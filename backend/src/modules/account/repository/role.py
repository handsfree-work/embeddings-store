from sqlalchemy import select

from src.modules.account.models.db.permission import PermissionEntity, Permission
from src.modules.account.models.db.role import Role, RoleEntity
from src.modules.account.models.db.role_permission import RolePermission
from src.modules.account.repository.permission import PermissionRepository
from src.modules.account.repository.role_permission import RolePermissionRepository
from src.repository.crud import BaseCRUDRepository
from src.repository.schema import SelectOptions


class RoleRepository(BaseCRUDRepository[Role, RoleEntity]):
    model = Role
    pass

    def __init__(self, session_wrapper):
        super().__init__(session_wrapper)
        self.permission_repo = PermissionRepository(session_wrapper=session_wrapper)
        self.role_permission_repo = RolePermissionRepository(session_wrapper=session_wrapper)

    async def check_permission(self, roles: list[int], per: str):
        return True

    async def get_permissions(self, role_ids) -> list[PermissionEntity]:
        permissions = await self.permission_repo.find(options=SelectOptions().with_where(Permission.id.in_(
            select(RolePermission.permission_id).where(RolePermission.role_id.in_(role_ids)))))
        return permissions

    async def get_permission_ids(self, id):
        role_permissions = await self.role_permission_repo.find(
            options=SelectOptions().with_where(RolePermission.role_id == id))
        return [role_permission.permission_id for role_permission in role_permissions]

    async def authz(self, role_id, permission_ids):
        await self.role_permission_repo.delete_where(
            options=SelectOptions().with_where(RolePermission.role_id == role_id))
        session = self.get_session()
        all = []
        for permission_id in permission_ids:
            create_bean = RolePermission(role_id=role_id, permission_id=permission_id)
            all.append(create_bean)

        session.add_all(all)
        session.bulk_insert_mappings(RolePermission, all)
        await session.flush()
