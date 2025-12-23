"""add numero action

Revision ID: 17b9e53d372c
Revises: 71d5d63bdcab
Create Date: 2025-02-11 05:52:06.306531

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "17b9e53d372c"
down_revision: Union[str, None] = "71d5d63bdcab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "action", sa.Column("numero_action", sa.Integer(), nullable=False, server_default="1")
    )
    op.drop_constraint("action_id_project_fkey", "action", type_="foreignkey")
    op.create_foreign_key(None, "action", "project", ["id_project"], ["id_project"])
    op.drop_constraint("user_action_id_user_fkey", "user_action", type_="foreignkey")
    op.create_foreign_key(None, "user_action", "user", ["id_user"], ["id_user"])
    op.drop_constraint("user_action_time_id_user_fkey", "user_action_time", type_="foreignkey")
    op.drop_constraint("user_action_time_id_action_fkey", "user_action_time", type_="foreignkey")
    op.create_foreign_key(None, "user_action_time", "user", ["id_user"], ["id_user"])
    op.create_foreign_key(None, "user_action_time", "action", ["id_action"], ["id_action"])


def downgrade() -> None:
    op.drop_constraint(None, "user_action_time", type_="foreignkey")
    op.drop_constraint(None, "user_action_time", type_="foreignkey")
    op.create_foreign_key(
        "user_action_time_id_action_fkey",
        "user_action_time",
        "action",
        ["id_action"],
        ["id_action"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "user_action_time_id_user_fkey",
        "user_action_time",
        "user",
        ["id_user"],
        ["id_user"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "user_action", type_="foreignkey")
    op.create_foreign_key(
        "user_action_id_user_fkey",
        "user_action",
        "user",
        ["id_user"],
        ["id_user"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "action", type_="foreignkey")
    op.create_foreign_key(
        "action_id_project_fkey",
        "action",
        "project",
        ["id_project"],
        ["id_project"],
        ondelete="CASCADE",
    )
    op.drop_column("action", "numero_action")
