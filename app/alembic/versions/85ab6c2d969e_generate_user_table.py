"""generate user table

Revision ID: 85ab6c2d969e
Revises: 8d5920d0bd1d
Create Date: 2024-08-20 12:54:29.571079

"""

from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from schemas.user import get_password_hash
from shared.settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision: str = "85ab6c2d969e"
down_revision: Union[str, None] = "8d5920d0bd1d"
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
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("company_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
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
                "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("users")
