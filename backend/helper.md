```shell
# 创建一个新的数据库迁移版本
alembic revision --autogenerate -m "YOUR MIGRATION TITLE"  --config alembic.ini
# 升级数据库版本
alembic upgrade head    # to register the database classes


```