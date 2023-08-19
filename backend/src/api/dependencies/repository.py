import typing

from fastapi import Depends

from src.repository.session import get_session_wrapper
from src.repository.crud import BaseRepository, SessionWrapper


def get_repository(
        repo_type: typing.Type[BaseRepository],
) -> typing.Callable[[SessionWrapper], BaseRepository]:
    def _get_repo(
            session_wrapper: SessionWrapper = Depends(get_session_wrapper, use_cache=True),
    ) -> BaseRepository:
        return repo_type(session_wrapper=session_wrapper)

    return _get_repo
