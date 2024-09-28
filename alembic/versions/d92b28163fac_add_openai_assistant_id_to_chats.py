"""add openai_assistant_id to chats

Revision ID: d92b28163fac
Revises: b9719074d775
Create Date: 2024-09-28 14:44:34.374016

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd92b28163fac'
down_revision: Union[str, None] = 'b9719074d775'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chats', sa.Column('openai_assistant_id', sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_column('chats', 'openai_assistant_id')
