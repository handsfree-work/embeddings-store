import fastapi
from fastapi import HTTPException


class ServerException(HTTPException):
    code: int

    def __init__(
            self,
            code: int,
            status_code: int = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            message: str = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message)
        self.code = code


def server_error(code: int = 500, message: str = "server error") -> Exception:
    return ServerException(
        code=code,
        message=message,
    )


def client_error(code: int = 400, message: str = "bad request") -> Exception:
    return ServerException(
        code=code,
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        message=message,
    )
