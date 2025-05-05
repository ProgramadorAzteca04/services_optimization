"""baseline

Revision ID: 034627a711f2
Revises: 70441c72789d
Create Date: 2025-05-05 13:17:39.643780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '034627a711f2'
down_revision: Union[str, None] = '70441c72789d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
