"""create assistants table

Revision ID: ec2d5510ff30
Revises: 95e9f7524379
Create Date: 2024-09-19 19:41:13.002081

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ec2d5510ff30'
down_revision: Union[str, None] = '95e9f7524379'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assistants",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("desc", sa.Text(), nullable=False, default=""),
        sa.Column("icon_url", sa.Text(), nullable=False),
        sa.Column("color", sa.Text(), nullable=False),
        sa.Column("instruction", sa.Text(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("assistants")
