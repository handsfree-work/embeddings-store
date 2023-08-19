from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException


def exc_to_str(exc: Exception) -> str:
    if isinstance(exc, StarletteHTTPException) or isinstance(exc, HTTPException):
        return exc.detail
    return str(exc)
