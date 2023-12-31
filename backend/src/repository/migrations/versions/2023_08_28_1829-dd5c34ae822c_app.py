"""app

Revision ID: dd5c34ae822c
Revises: fc947874739f
Create Date: 2023-08-28 18:29:09.489290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table

from src.modules.account.models.db.permission import Permission
from src.repository.migrations.utils import get_permission_id

# revision identifiers, used by Alembic.
revision = 'dd5c34ae822c'
down_revision = 'fc947874739f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('em_app',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('title', sa.String(length=500), nullable=False),
                    sa.Column('app_id', sa.String(length=100), nullable=False, unique=True),
                    sa.Column('app_key', sa.String(length=512), nullable=False, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    permission_table = Table('sys_permission', Permission.metadata)

    # admin_id = 1

    # op.bulk_insert(permission_table, [
    #     {'title': '嵌入管理', 'code': 'embeddings', 'parent_id': admin_id},
    # ])

    em_id = get_permission_id(op, "embeddings")
    print("em_id", em_id)
    op.bulk_insert(permission_table, [
        {'title': 'APP管理', 'code': 'embeddings:app', 'parent_id': em_id},
    ])

    parent_id = get_permission_id(op, "embeddings:app")
    op.bulk_insert(permission_table, [
        {'title': '查看', 'code': 'embeddings:app:view', 'parent_id': parent_id},
        {'title': '添加', 'code': 'embeddings:app:add', 'parent_id': parent_id},
        {'title': '修改', 'code': 'embeddings:app:update', 'parent_id': parent_id},
        {'title': '删除', 'code': 'embeddings:app:delete', 'parent_id': parent_id},
    ])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('em_app')
    # ### end Alembic commands ###
