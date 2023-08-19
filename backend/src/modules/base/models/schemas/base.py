import pydantic


class BaseSchemaModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        from_attributes: bool = True
        validate_assignment: bool = True
        populate_by_name: bool = True


class BaseAnyModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        arbitrary_types_allowed: bool = True
