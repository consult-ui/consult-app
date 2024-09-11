"""create refresh sessions table

Revision ID: cfcec78b3f20
Revises: 4ca9545577e9
Create Date: 2024-09-11 11:16:42.815332

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cfcec78b3f20'
down_revision: Union[str, None] = '4ca9545577e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_sessions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("refresh_token", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("expires_in", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("refresh_sessions")
