from fastapi import FastAPI

from src.initial.exception_handler import register_exception_handler
from src.initial.middlewares import add_middlewares
from src.securities.hashing.password import pwd_generator


def on_start(app: FastAPI):
    add_middlewares(app)
    register_exception_handler(app)
    # 打印一个随机密码，你可以根据此日志重置管理员密码
    pwd_generator.random_password()
