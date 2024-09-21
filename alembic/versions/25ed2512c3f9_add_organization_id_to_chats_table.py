"""add organization_id to chats table

Revision ID: 25ed2512c3f9
Revises: ec2d5510ff30
Create Date: 2024-09-21 13:28:23.018571

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '25ed2512c3f9'
down_revision: Union[str, None] = 'ec2d5510ff30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "chats",
        sa.Column("organization_id", sa.BigInteger, sa.ForeignKey("organizations.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("chats", "organization_id")
