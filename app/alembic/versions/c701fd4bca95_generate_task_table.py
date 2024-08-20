"""generate task table

Revision ID: c701fd4bca95
Revises: 85ab6c2d969e
Create Date: 2024-08-20 12:54:36.832365

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import ENUM

from shared.enums.index import TaskPriority, TaskStatus


# revision identifiers, used by Alembic.
revision: str = "c701fd4bca95"
down_revision: Union[str, None] = "85ab6c2d969e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


task_status_enum = ENUM(TaskStatus, name="task_status", create_type=False)
task_priority_enum = ENUM(TaskPriority, name="task_priority", create_type=False)


def upgrade() -> None:
    # Create ENUM types if they do not already exist
    task_status_enum.create(op.get_bind())
    task_priority_enum.create(op.get_bind())

    # Create the tasks table with enum default values as strings
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "status",
            task_status_enum,
            nullable=False,
            server_default=str(TaskStatus.ACTIVE.value),  # Convert enum value to string
        ),
        sa.Column(
            "priority",
            task_priority_enum,
            nullable=False,
            server_default=str(
                TaskPriority.HIGHEST.value
            ),  # Convert enum value to string
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Drop the tasks table
    op.drop_table("tasks")

    # Drop ENUM types if they exist
    op.execute("DROP TYPE IF EXISTS task_status;")
    op.execute("DROP TYPE IF EXISTS task_priority;")
