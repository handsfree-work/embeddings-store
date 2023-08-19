@echo off
set /p title=MIGRATION_TITLE:
echo title is: %title%

alembic revision --autogenerate -m "%title%"

alembic upgrade head