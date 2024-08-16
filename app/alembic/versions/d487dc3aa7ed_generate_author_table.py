"""generate author table

Revision ID: d487dc3aa7ed
Revises: 
Create Date: 2024-08-16 15:59:53.153400

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.author import Gender


# revision identifiers, used by Alembic.
revision: str = "d487dc3aa7ed"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column(
            "gender",
            sa.Enum(Gender, name="gender"),
            nullable=False,
            server_default="NONE",
        ),  # Update the default value
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("authors")
    op.execute("DROP TYPE gender;")
