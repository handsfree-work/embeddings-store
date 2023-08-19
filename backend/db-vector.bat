@echo off
set /p title=MIGRATION_TITLE:
echo title is: %title%

alembic -c "alembic-pgvector.ini" revision  --autogenerate -m "%title%"

alembic -c "alembic-pgvector.ini" upgrade head