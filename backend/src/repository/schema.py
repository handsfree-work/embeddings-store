from pydantic import BaseModel

from src.modules.base.models.schemas.base import BaseSchemaModel


class OrderBy(BaseModel):
    name: str
    desc: bool


class SelectOptions:

    def __init__(self):
        self.selectinload: list[any] = list()
        self.joinedload: list[any] = list()
        self.order_by: list[OrderBy] = list()
        self.limit: int = -1
        self.offset: int = 0
        self.wheres: list[any] = list()
        self.query: any = None

    def with_query(self, query: any):
        self.query = query
        return self

    def clear_load(self):
        self.selectinload.clear()
        self.joinedload.clear()
        return self

    def with_selectinload(self, column_opts: any):
        self.selectinload.append(column_opts)
        return self

    def with_joinedload(self, column_opts: any):
        self.joinedload.append(column_opts)
        return self

    def with_order_by(self, order_by: OrderBy):
        self.order_by.append(order_by)
        return self

    def with_limit(self, limit: int):
        self.limit = limit
        return self

    def with_offset(self, offset: int):
        self.offset = offset
        return self

    def with_where(self, where: any):
        self.wheres.append(where)
        return self

    def has_relation(self, key):
        if len(self.selectinload) > 0:
            for item in self.selectinload:
                if item.key == key:
                    return True
        if len(self.joinedload) > 0:
            for item in self.joinedload:
                if item.key == key:
                    return True
        pass
