"""generate book table

Revision ID: 601a1fbfd574
Revises: d487dc3aa7ed
Create Date: 2024-08-16 16:01:08.715158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '601a1fbfd574'
down_revision: Union[str, None] = 'd487dc3aa7ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
