import fastapi
import loguru
import starlette.exceptions
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import ClientDisconnect
from starlette.responses import JSONResponse

from src.modules.base.models.schemas.response import RestfulRes
from src.utilities.exceptions.biz.biz_common import ServerException
from src.utilities.formatters.array_formatter import format_array_to_string


async def exception_handler(request, exc):
    if isinstance(exc, ClientDisconnect):
        return
    if isinstance(exc, HTTPException) or isinstance(exc, starlette.exceptions.HTTPException):
        return JSONResponse(RestfulRes(code=exc.status_code, message=exc.detail, data=None).model_dump(),
                            status_code=exc.status_code)
    if isinstance(exc, RequestValidationError):
        error = exc.errors()[0]
        message = error['msg'] + ' : ' + format_array_to_string(error['loc'], '.')
        return JSONResponse(RestfulRes(code=400, message=message, data=None).model_dump(),
                            status_code=400)
    if isinstance(exc, ServerException):
        return JSONResponse(RestfulRes(code=exc.code, message=exc.detail, data=None).model_dump(),
                            status_code=exc.status_code)
    loguru.logger.opt(exception=exc).error('未知异常')
    return JSONResponse(RestfulRes[str].error("服务器内部错误").model_dump(), status_code=500)


def register_exception_handler(app: fastapi.FastAPI):
    app.add_exception_handler(ServerException, exception_handler)
    app.add_exception_handler(RequestValidationError, exception_handler)
    app.add_exception_handler(HTTPException, exception_handler)
    app.add_exception_handler(starlette.exceptions.HTTPException, exception_handler)
    app.add_exception_handler(Exception, exception_handler)
