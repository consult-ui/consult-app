"""drop old contact_request table and create new one

Revision ID: cd85b4918dcc
Revises: aa0793c280ea
Create Date: 2024-09-26 22:38:13.981282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd85b4918dcc'
down_revision: Union[str, None] = 'aa0793c280ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.drop_table("contact_request")

    op.create_table(
        "contact_request",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("email", sa.Text(), nullable=True),
        sa.Column("phone_number", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("is_processed", sa.Boolean(), default=False),
    )



def downgrade() -> None:
    op.drop_table("contact_request")
