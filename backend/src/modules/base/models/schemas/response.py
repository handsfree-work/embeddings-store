from typing import TypeVar, Generic, List, Optional

from pydantic import BaseModel

from src.modules.base.models.schemas.base import BaseSchemaModel
from src.repository.schema import OrderBy

T = TypeVar('T')  # 泛型类型 T


class Pager(BaseSchemaModel):
    offset: int = 0
    limit: int = 20
    total: int | None = None


class PageQuery(BaseSchemaModel, Generic[T]):
    pager: Pager = Pager()
    order_by: List[OrderBy] | None = None
    query: T | None = None


class PageRes(BaseSchemaModel, Generic[T]):
    pager: Pager
    order_by: List[OrderBy] | None
    list: Optional[List[T]] = []


class ListRes(BaseSchemaModel, Generic[T]):
    list: Optional[List[T]] = []


class RestfulRes(BaseSchemaModel, Generic[T]):
    code: int = 0
    message: str = ""
    data: T | None = None

    @staticmethod
    def success(message: str = 'success', data: T | None = None):
        return RestfulRes(code=0, message=message, data=data)

    @staticmethod
    def success_list(data: any = None):
        return RestfulRes(code=0, message='success', data=ListRes(list=data))

    @staticmethod
    def error(message: str = 'server error'):
        return RestfulRes(code=1, message=message, data=None)
