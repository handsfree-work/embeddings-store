from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from src.api.dependencies.repository import get_repository
from src.modules.embeddings.repository.app import AppRepository
from src.utilities.exceptions.http.exc_401 import http_exc_401

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


class EmTokenChecker:
    def __init__(self):
        pass

    async def __call__(self, request: Request, token: str = Depends(oauth2_schema),
                       app_repo: AppRepository = Depends(get_repository(repo_type=AppRepository))
                       ):
        # check token
        passed = await app_repo.check_token(token)
        if not passed:
            raise http_exc_401(detail="token is invalid")
