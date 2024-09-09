"""add password hash to users

Revision ID: 4ca9545577e9
Revises: c4b8933e2259
Create Date: 2024-09-09 21:55:23.173768

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ca9545577e9"
down_revision: Union[str, None] = "c4b8933e2259"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password", sa.Text, nullable=False))


def downgrade() -> None:
    op.drop_column("users", "password")
