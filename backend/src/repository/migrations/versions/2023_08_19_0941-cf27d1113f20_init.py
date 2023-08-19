"""init

Revision ID: cf27d1113f20
Revises: 
Create Date: 2023-08-19 09:41:49.919928

"""
import datetime

from alembic import op
import sqlalchemy as sa

from src.securities.hashing.password import pwd_generator

# revision identifiers, used by Alembic.
revision = 'cf27d1113f20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    permission_table =  op.create_table('sys_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('code', sa.String(length=64), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    role_table = op.create_table('sys_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    role_permission_table = op.create_table('sys_role_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    user_table = op.create_table('sys_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('_hashed_password', sa.String(length=1024), nullable=True),
    sa.Column('_hash_salt', sa.String(length=1024), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_logged_in', sa.Boolean(), nullable=False),
    sa.Column('user_type', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    user_role_table = op.create_table('sys_user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    password = "123456"
    hash_salt = pwd_generator.generate_salt
    hashed_password = pwd_generator.generate_hashed_password(hash_salt, password)
    op.bulk_insert(user_table, [{
        'username': 'admin',
        'email': 'admin@localhost.com',
        'is_verified': True,
        'is_active': True,
        'is_logged_in': False,
        'user_type': 1,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
        'password': password,
        '_hashed_password': hashed_password,
        '_hash_salt': hash_salt
    }])

    op.bulk_insert(role_table, [{
        'name': 'admin',
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now()
    }])
    op.bulk_insert(user_role_table, [{
        'user_id': 1,
        'role_id': 1
    }])

    op.bulk_insert(permission_table, [
        {'title': '管理后台', 'code': 'admin', 'parent_id': 0},
        {'title': '主页', 'code': 'index', 'parent_id': 1},
        {'title': '系统管理', 'code': 'sys', 'parent_id': 1},
        {'title': '账户管理', 'code': 'authority', 'parent_id': 3},
        {'title': '用户管理', 'code': 'authority:user', 'parent_id': 4},
        {'title': '用户查看', 'code': 'authority:user:view', 'parent_id': 5},
        {'title': '用户添加', 'code': 'authority:user:add', 'parent_id': 5},
        {'title': '用户修改', 'code': 'authority:user:update', 'parent_id': 5},
        {'title': '用户删除', 'code': 'authority:user:delete', 'parent_id': 5},
        {'title': '用户授权', 'code': 'authority:user:authz', 'parent_id': 5},
        {'title': '角色管理', 'code': 'authority:role', 'parent_id': 4},
        {'title': '角色查看', 'code': 'authority:role:view', 'parent_id': 11},
        {'title': '角色添加', 'code': 'authority:role:add', 'parent_id': 11},
        {'title': '角色修改', 'code': 'authority:role:update', 'parent_id': 11},
        {'title': '角色删除', 'code': 'authority:role:delete', 'parent_id': 11},
        {'title': '角色授权', 'code': 'authority:role:authz', 'parent_id': 11},
        {'title': '权限管理', 'code': 'authority:permission', 'parent_id': 4},
        {'title': '权限查看', 'code': 'authority:permission:view', 'parent_id': 17},
        {'title': '权限添加', 'code': 'authority:permission:add', 'parent_id': 17},
        {'title': '权限修改', 'code': 'authority:permission:update', 'parent_id': 17},
        {'title': '权限删除', 'code': 'authority:permission:delete', 'parent_id': 17},

    ])
    op.bulk_insert(role_permission_table, [
        {'role_id': 1, 'permission_id': 1},
        {'role_id': 1, 'permission_id': 2},
        {'role_id': 1, 'permission_id': 3},
        {'role_id': 1, 'permission_id': 4},
        {'role_id': 1, 'permission_id': 5},
        {'role_id': 1, 'permission_id': 6},
        {'role_id': 1, 'permission_id': 7},
        {'role_id': 1, 'permission_id': 8},
        {'role_id': 1, 'permission_id': 9},
        {'role_id': 1, 'permission_id': 10},
        {'role_id': 1, 'permission_id': 11},
        {'role_id': 1, 'permission_id': 12},
        {'role_id': 1, 'permission_id': 13},
        {'role_id': 1, 'permission_id': 14},
        {'role_id': 1, 'permission_id': 15},
        {'role_id': 1, 'permission_id': 16},
        {'role_id': 1, 'permission_id': 17},
        {'role_id': 1, 'permission_id': 18},
        {'role_id': 1, 'permission_id': 19},
        {'role_id': 1, 'permission_id': 20},
        {'role_id': 1, 'permission_id': 21},
    ])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sys_user_role')
    op.drop_table('sys_user')
    op.drop_table('sys_role_permission')
    op.drop_table('sys_role')
    op.drop_table('sys_permission')
    # ### end Alembic commands ###
