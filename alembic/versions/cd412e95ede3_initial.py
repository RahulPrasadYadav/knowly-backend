"""initial

Revision ID: cd412e95ede3
Revises: 
Create Date: 2026-07-18 02:15:48.295691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd412e95ede3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline revision: database is assumed to already match the current models."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
