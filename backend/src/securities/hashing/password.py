from src.securities.hashing.hash import hash_generator
from src.utilities.strings.strings import random_number_string
import loguru


class PasswordGenerator:
    @property
    def generate_salt(self) -> str:
        return hash_generator.generate_password_salt_hash

    def generate_hashed_password(self, hash_salt: str, new_password: str) -> str:
        return hash_generator.generate_password_hash(hash_salt=hash_salt, password=new_password)

    def is_password_authenticated(self, hash_salt: str, password: str, hashed_password: str) -> bool:
        return hash_generator.is_password_verified(password=hash_salt + password, hashed_password=hashed_password)

    def random_password(self):
        password = random_number_string(6)
        salt = self.generate_salt
        loguru.logger.info("随机密码,你可以根据此日志重置管理员密码:password={}，hashed_password={}，salt={}",
                           password,
                           self.generate_hashed_password(
                               hash_salt=salt, new_password=password
                           ),
                           salt)


def get_pwd_generator() -> PasswordGenerator:
    return PasswordGenerator()


pwd_generator: PasswordGenerator = get_pwd_generator()
