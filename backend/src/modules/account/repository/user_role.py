from src.modules.account.models.db.user_role import UserRole, UserRoleEntity
from src.repository.crud import BaseCRUDRepository


class UserRoleRepository(BaseCRUDRepository[UserRole, UserRoleEntity]):
    model = UserRole
    pass
