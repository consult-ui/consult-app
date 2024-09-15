"""organization cascase delete user_organizations

Revision ID: 0f325784201f
Revises: 562b8aea9741
Create Date: 2024-09-15 17:52:03.592115

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0f325784201f'
down_revision: Union[str, None] = '562b8aea9741'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    -- Удаляем существующее ограничение внешнего ключа
ALTER TABLE user_organizations
DROP CONSTRAINT user_organizations_organization_id_fkey;

-- Добавляем новое ограничение с ON DELETE CASCADE
ALTER TABLE user_organizations
ADD CONSTRAINT user_organizations_organization_id_fkey
FOREIGN KEY (organization_id)
REFERENCES organizations (id)
ON DELETE CASCADE;

    """)


def downgrade() -> None:
    pass
