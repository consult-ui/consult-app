"""create organization table

Revision ID: 568c2c5fd2d1
Revises: 1f6952f8ee18
Create Date: 2024-09-15 01:54:12.881473

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '568c2c5fd2d1'
down_revision: Union[str, None] = '1f6952f8ee18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("activity_type", sa.Text(), nullable=False),
        sa.Column("tax_number", sa.Text(), nullable=True),
        sa.Column("head_name", sa.Text(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("quarterly_income", sa.BigInteger(), nullable=True),
        sa.Column("quarterly_expenses", sa.BigInteger(), nullable=True),
        sa.Column("number_employees", sa.BigInteger(), nullable=True),
        sa.Column("average_receipt", sa.BigInteger(), nullable=True),
        sa.Column("context", sa.Text(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()"),
                  nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("organizations")
