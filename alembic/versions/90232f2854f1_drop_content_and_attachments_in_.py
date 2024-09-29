"""drop content and attachments in messages table

Revision ID: 90232f2854f1
Revises: 95a5877b8266
Create Date: 2024-09-29 16:15:32.877427

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '90232f2854f1'
down_revision: Union[str, None] = '95a5877b8266'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('messages', 'content')
    op.drop_column('messages', 'attachments')
    op.add_column("messages", sa.Column("openai_message", JSONB, nullable=False))


def downgrade() -> None:
    pass
