import typing

import loguru
import sqlalchemy
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.modules.account.models.db.permission import PermissionEntity
from src.modules.account.models.db.user import User
from src.modules.account.models.db.user_role import UserRoleEntity, UserRole
from src.modules.account.models.schemas.user import UserInCreate, UserInLogin, UserInUpdate, UserEntity
from src.modules.account.repository.permission import PermissionRepository
from src.modules.account.repository.role import RoleRepository
from src.modules.account.repository.user_role import UserRoleRepository
from src.repository.crud import BaseCRUDRepository
from src.repository.schema import SelectOptions
from src.securities.hashing.password import pwd_generator
from src.securities.verifications.credentials import credential_verifier
from src.utilities.exceptions.biz.biz_common import client_error
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from src.utilities.exceptions.password import PasswordDoesNotMatch


class UserRepository(BaseCRUDRepository[User, UserEntity]):
    model = User

    def __init__(self, session_wrapper):
        super().__init__(session_wrapper)
        self.permission_repo = PermissionRepository(session_wrapper=session_wrapper)
        self.user_role_repo = UserRoleRepository(session_wrapper=session_wrapper)
        self.role_repo = RoleRepository(session_wrapper=session_wrapper)

    async def create_user(self, account_create: UserInCreate) -> UserEntity:
        new_user = User(username=account_create.username, email=account_create.email, is_logged_in=True)

        new_user.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_user.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_user.hash_salt, new_password=account_create.password
            )
        )

        self.get_session().add(instance=new_user)
        await self.get_session().commit()
        await self.get_session().refresh(instance=new_user)

        return new_user.to_entity()

    async def read_accounts(self) -> typing.Sequence[User]:
        stmt = sqlalchemy.select(User)
        query = await self.get_session().execute(statement=stmt)
        return query.scalars().all()

    async def read_account_by_id(self, id: int) -> User:
        stmt = sqlalchemy.select(User).where(User.id == id)
        query = await self.get_session().execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")

        return query.scalar()

    async def read_account_by_username(self, username: str) -> User:
        stmt = sqlalchemy.select(User).where(User.username == username)
        query = await self.get_session().execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with username `{username}` does not exist!")

        return query.scalar()

    async def read_account_by_email(self, email: str) -> User:
        stmt = sqlalchemy.select(User).where(User.email == email)
        query = await self.get_session().execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with email `{email}` does not exist!")

        return query.scalar()

    async def read_user_by_password_authentication(self, account_login: UserInLogin) -> UserEntity:
        db_account = await self.get_user_by_username(account_login.username)
        if db_account is None:
            raise EntityDoesNotExist("Wrong username or wrong email!")

        loguru.logger.error("password:{}", pwd_generator.generate_hashed_password(
            hash_salt=db_account.hash_salt, new_password=account_login.password
        ))
        if not pwd_generator.is_password_authenticated(hash_salt=db_account.hash_salt, password=account_login.password,
                                                       hashed_password=db_account.hashed_password):
            raise PasswordDoesNotMatch("Password does not match!")

        entity = db_account.to_entity()
        entity.role_ids = await self.get_role_ids(db_account.id)
        return entity

    async def update_account_by_id(self, id: int, account_update: UserInUpdate) -> User:
        new_account_data = account_update.model_dump()

        select_stmt = sqlalchemy.select(User).where(User.id == id)
        query = await self.get_session().execute(statement=select_stmt)
        update_account = query.scalar()

        if not update_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")

        update_stmt = sqlalchemy.update(table=User).where(User.id == update_account.id).values(
            updated_at=sqlalchemy_functions.now())

        if new_account_data["username"]:
            update_stmt = update_stmt.values(username=new_account_data["username"])

        if new_account_data["email"]:
            update_stmt = update_stmt.values(username=new_account_data["email"])

        if new_account_data["password"]:
            update_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
            update_account.set_hashed_password(
                hashed_password=pwd_generator.generate_hashed_password(hash_salt=update_account.hash_salt,
                                                                       new_password=new_account_data[
                                                                           "password"]))

        await self.get_session().execute(statement=update_stmt)
        await self.get_session().commit()
        await self.get_session().refresh(instance=update_account)

        return update_account

    async def delete_account_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(User).where(User.id == id)
        query = await self.get_session().execute(statement=select_stmt)
        delete_account = query.scalar()

        if not delete_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")

        stmt = sqlalchemy.delete(table=User).where(User.id == delete_account.id)

        await self.get_session().execute(statement=stmt)
        await self.get_session().commit()

        return f"Account with id '{id}' is successfully deleted!"

    async def is_username_taken(self, username: str) -> bool:
        username_stmt = sqlalchemy.select(User.username).select_from(User).where(User.username == username)
        username_query = await self.get_session().execute(username_stmt)
        db_username = username_query.scalar()

        if not credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")

        return True

    async def is_email_taken(self, email: str) -> bool:
        email_stmt = sqlalchemy.select(User.email).select_from(User).where(User.email == email)
        email_query = await self.get_session().execute(email_stmt)
        db_email = email_query.scalar()

        if not credential_verifier.is_email_available(email=db_email):
            raise EntityAlreadyExists(f"The email `{email}` is already registered!")

        return True

    async def get_permissions(self, user_id: int) -> list[PermissionEntity]:
        user = await self.get(id=user_id)
        if user is None:
            raise client_error(message=f"User with id `{user_id}` does not exist!")
        user_roles = await self.user_role_repo.find(condition=UserRoleEntity(user_id=user_id))
        role_ids = [user_role.role_id for user_role in user_roles]
        permissions = await self.role_repo.get_permissions(role_ids)
        return permissions

    async def get_with_role_ids(self, id: int):
        user = await self.get(id=id)
        role_ids = await self.get_role_ids(id)
        user.role_ids = role_ids
        return user

    async def get_role_ids(self, id):
        user_roles = await self.user_role_repo.find(condition=UserRoleEntity(user_id=id))
        return [user_role.role_id for user_role in user_roles]

    async def update_with_roles(self, id, user):
        await self.update(id=id, entity=user)
        await self.user_role_repo.delete_where(options=SelectOptions().with_where(UserRole.user_id == id))
        for role_id in user.role_ids:
            await self.user_role_repo.create(UserRoleEntity(user_id=id, role_id=role_id))
        pass

    async def get_user_by_username(self, username):
        stmt = sqlalchemy.select(User).where(User.username == username)
        query = await self.get_session().execute(statement=stmt)
        return query.scalar()
