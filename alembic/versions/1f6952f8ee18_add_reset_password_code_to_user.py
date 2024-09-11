"""add reset_password_code to user

Revision ID: 1f6952f8ee18
Revises: ecf4aa826d5d
Create Date: 2024-09-11 22:24:04.633195

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1f6952f8ee18'
down_revision: Union[str, None] = 'ecf4aa826d5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('reset_password_code', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'reset_password_code')
