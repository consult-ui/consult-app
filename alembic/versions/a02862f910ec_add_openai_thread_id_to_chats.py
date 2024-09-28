"""add openai_thread_id to chats

Revision ID: a02862f910ec
Revises: d92b28163fac
Create Date: 2024-09-28 15:28:51.043631

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a02862f910ec'
down_revision: Union[str, None] = 'd92b28163fac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("chats", sa.Column("openai_thread_id", sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_column("chats", "openai_thread_id")
