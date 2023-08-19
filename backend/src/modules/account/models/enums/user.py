from enum import Enum


class UserType(Enum):
    admin = 1
    member = 2


UserType.admin.label = "管理员"
UserType.member.label = "用户"


def enum_values_array_to_json(enumObj: Enum):
    return [enum.value for enum in enumObj]
