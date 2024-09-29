"""create openai_id index on files table

Revision ID: 95a5877b8266
Revises: 0ecc118a3db0
Create Date: 2024-09-29 13:59:31.819664

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '95a5877b8266'
down_revision: Union[str, None] = '0ecc118a3db0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_files_openai_id', 'files', ['openai_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_files_openai_id', table_name='files')
