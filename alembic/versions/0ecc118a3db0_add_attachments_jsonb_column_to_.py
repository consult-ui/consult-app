"""add attachments jsonb column to messages table

Revision ID: 0ecc118a3db0
Revises: bf0960fce93c
Create Date: 2024-09-28 18:13:01.443812

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '0ecc118a3db0'
down_revision: Union[str, None] = 'bf0960fce93c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('attachments', JSONB(), nullable=False, server_default='[]'))


def downgrade() -> None:
    op.drop_column('messages', 'attachments')
