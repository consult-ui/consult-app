"""Add new fields to User model

Revision ID: dc787578e1da
Revises: 0f325784201f
Create Date: 2024-09-17 18:17:41.208498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc787578e1da'
down_revision: Union[str, None] = '0f325784201f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('whatsapp_url', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('telegram_url', sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'whatsapp_url')
    op.drop_column('users', 'telegram_url')
