"""questions

Revision ID: 6518d2fd9b98
Revises: 25a9ee90b3b9
Create Date: 2024-10-05 16:40:16.209922

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6518d2fd9b98'
down_revision: Union[str, None] = '25a9ee90b3b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    op.drop_constraint('chats_organization_id_fkey', 'chats', type_='foreignkey')
    op.create_foreign_key(None, 'chats', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'chats', 'organizations', ['organization_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('files_chat_id_fkey', 'files', type_='foreignkey')
    op.create_foreign_key(None, 'files', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('refresh_sessions_user_id_fkey', 'refresh_sessions', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_sessions', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'refresh_sessions', type_='foreignkey')
    op.create_foreign_key('refresh_sessions_user_id_fkey', 'refresh_sessions', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_chat_id_fkey', 'messages', 'chats', ['chat_id'], ['id'])
    op.drop_constraint(None, 'files', type_='foreignkey')
    op.create_foreign_key('files_chat_id_fkey', 'files', 'chats', ['chat_id'], ['id'])
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.create_foreign_key('chats_organization_id_fkey', 'chats', 'organizations', ['organization_id'], ['id'])
    op.create_foreign_key('chats_user_id_fkey', 'chats', 'users', ['user_id'], ['id'])
