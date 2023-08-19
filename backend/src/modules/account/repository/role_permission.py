from src.modules.account.models.db.role_permission import RolePermission, RolePermissionEntity
from src.repository.crud import BaseCRUDRepository


class RolePermissionRepository(BaseCRUDRepository[RolePermission, RolePermissionEntity]):
    model = RolePermission
    pass


