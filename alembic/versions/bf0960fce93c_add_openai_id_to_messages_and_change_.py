"""add openai_id to messages and change content to jsonb

Revision ID: bf0960fce93c
Revises: a02862f910ec
Create Date: 2024-09-28 17:19:05.392218

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bf0960fce93c'
down_revision: Union[str, None] = 'a02862f910ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('openai_id', sa.Text(), nullable=False))
    op.alter_column('messages', 'content', type_=sa.JSONB(), nullable=False)


def downgrade() -> None:
    op.drop_column('messages', 'openai_id')
    op.alter_column('messages', 'content', type_=sa.JSONB(), nullable=False)
