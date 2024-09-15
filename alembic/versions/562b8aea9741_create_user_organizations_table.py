"""create user organizations table

Revision ID: 562b8aea9741
Revises: 568c2c5fd2d1
Create Date: 2024-09-15 14:24:55.967799

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '562b8aea9741'
down_revision: Union[str, None] = '568c2c5fd2d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_organizations",
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("organization_id", sa.BigInteger, sa.ForeignKey("organizations.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("user_organizations")
