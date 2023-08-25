from sqlalchemy import text


def get_permission_id(op, code: str):
    result = op.get_bind().execute(text(f"SELECT id FROM sys_permission where code =\'{code}\'"))

    # 获取查询结果
    rows = result.fetchall()

    if len(rows) > 0:
        return rows[0][0]
    else:
        raise Exception(f"permission code {code} not found")
