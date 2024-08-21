"""generate company table

Revision ID: 8d5920d0bd1d
Revises: 
Create Date: 2024-08-20 12:54:21.724264

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.shared.enums import CompanyMode


# revision identifiers, used by Alembic.
revision: str = "8d5920d0bd1d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    company_table = op.create_table(
        "companies",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "mode",
            sa.Enum(CompanyMode, name="company_mode"),
            nullable=False,
            server_default=CompanyMode.ACTIVE.value,
        ),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("companies")
    op.execute("DROP TYPE company_mode;")
