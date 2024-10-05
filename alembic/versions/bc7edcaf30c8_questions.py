"""questions

Revision ID: bc7edcaf30c8
Revises: 90232f2854f1
Create Date: 2024-10-05 14:44:25.209529

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc7edcaf30c8'
down_revision: Union[str, None] = '90232f2854f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contact_requests',
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('email', sa.Text(), nullable=True),
                    sa.Column('phone_number', sa.Text(), nullable=True),
                    sa.Column('is_processed', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('contact_request')
    op.add_column('chats', sa.Column('questions', sa.ARRAY(sa.Text()), server_default='{}::text[]', nullable=False))
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    op.create_foreign_key(None, 'chats', 'users', ['user_id'], ['id'])
    op.drop_index('ix_files_openai_id', table_name='files')
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'chats', ['chat_id'], ['id'])
    op.drop_constraint('refresh_sessions_user_id_fkey', 'refresh_sessions', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_sessions', 'users', ['user_id'], ['id'])
    op.drop_constraint('user_organizations_organization_id_fkey', 'user_organizations', type_='foreignkey')
    op.create_foreign_key(None, 'user_organizations', 'organizations', ['organization_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'user_organizations', type_='foreignkey')
    op.create_foreign_key('user_organizations_organization_id_fkey', 'user_organizations', 'organizations',
                          ['organization_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'refresh_sessions', type_='foreignkey')
    op.create_foreign_key('refresh_sessions_user_id_fkey', 'refresh_sessions', 'users', ['user_id'], ['id'],
                          ondelete='CASCADE')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_chat_id_fkey', 'messages', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_files_openai_id', 'files', ['openai_id'], unique=True)
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.create_foreign_key('chats_user_id_fkey', 'chats', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('chats', 'questions')
    op.create_table('contact_request',
                    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('phone_number', sa.TEXT(), autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              autoincrement=False, nullable=False),
                    sa.Column('is_processed', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='contact_request_pkey')
                    )
    op.drop_table('contact_requests')
