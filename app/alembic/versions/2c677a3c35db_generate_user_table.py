"""generate user table

Revision ID: 2c677a3c35db
Revises: 601a1fbfd574
Create Date: 2024-08-19 10:07:02.357346

"""

from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from shared.settings import ADMIN_DEFAULT_PASSWORD
from schemas.user import get_password_hash


# revision identifiers, used by Alembic.
revision: str = "2c677a3c35db"
down_revision: Union[str, None] = "601a1fbfd574"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(length=255), unique=True, nullable=False),
        sa.Column("email", sa.String(), nullable=True, unique=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])

    # Date seed for first user
    op.bulk_insert(
        user_table,
        [
            {
                "id": str(uuid4()),
                "email": "admin@admin.com",
                "username": "admin",
                "first_name": "Admin",
                "last_name": "FastAPI",
                "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("users")
