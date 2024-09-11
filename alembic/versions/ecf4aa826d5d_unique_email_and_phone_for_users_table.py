"""unique email and phone for users table

Revision ID: ecf4aa826d5d
Revises: cfcec78b3f20
Create Date: 2024-09-11 11:23:16.143940

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ecf4aa826d5d'
down_revision: Union[str, None] = 'cfcec78b3f20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("unique_email", "users", ["email"])
    op.create_unique_constraint("unique_phone_number", "users", ["phone_number"])


def downgrade() -> None:
    op.drop_constraint("unique_email", "users")
    op.drop_constraint("unique_phone_number", "users")
