"""create files table

Revision ID: b9719074d775
Revises: cd85b4918dcc
Create Date: 2024-09-28 12:03:47.874665

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b9719074d775'
down_revision: Union[str, None] = 'cd85b4918dcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "files",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("chat_id", sa.BigInteger(), sa.ForeignKey("chats.id"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("openai_id", sa.Text(), nullable=False),
        sa.Column("size", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table("files")
