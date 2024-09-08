"""first

Revision ID: 7b333c3c1acc
Revises: 
Create Date: 2024-09-08 14:26:03.876564

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b333c3c1acc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("select 1;")


def downgrade() -> None:
    pass
