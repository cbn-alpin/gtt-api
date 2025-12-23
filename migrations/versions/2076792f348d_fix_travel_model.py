"""fix_travel_model

Revision ID: 2076792f348d
Revises: ec06874d5c81
Create Date: 2025-02-13 03:11:36.389097

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2076792f348d"
down_revision: Union[str, None] = "ec06874d5c81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("action_id_project_fkey", "action", type_="foreignkey")
    op.create_foreign_key(
        None, "action", "project", ["id_project"], ["id_project"], ondelete="CASCADE"
    )
    op.add_column(
        "travel",
        sa.Column("end_municipality", sa.String(length=50), nullable=False, server_default="RA"),
    )
    op.alter_column(
        "travel",
        "start_date",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "travel", "end_date", existing_type=sa.DATE(), type_=sa.DateTime(), existing_nullable=False
    )
    op.alter_column("travel", "status", existing_type=sa.VARCHAR(length=50), nullable=True)
    op.alter_column("travel", "meal_count", existing_type=sa.SMALLINT(), nullable=True)
    op.alter_column("travel", "license_vehicle", existing_type=sa.VARCHAR(length=12), nullable=True)
    op.alter_column("travel", "start_km", existing_type=sa.SMALLINT(), nullable=True)
    op.alter_column("travel", "end_km", existing_type=sa.SMALLINT(), nullable=True)
    op.drop_constraint("user_action_id_user_fkey", "user_action", type_="foreignkey")
    op.create_foreign_key(None, "user_action", "user", ["id_user"], ["id_user"], ondelete="CASCADE")
    op.drop_constraint("user_action_time_id_user_fkey", "user_action_time", type_="foreignkey")
    op.drop_constraint("user_action_time_id_action_fkey", "user_action_time", type_="foreignkey")
    op.create_foreign_key(
        None, "user_action_time", "action", ["id_action"], ["id_action"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "user_action_time", "user", ["id_user"], ["id_user"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(None, "user_action_time", type_="foreignkey")
    op.drop_constraint(None, "user_action_time", type_="foreignkey")
    op.create_foreign_key(
        "user_action_time_id_action_fkey",
        "user_action_time",
        "action",
        ["id_action"],
        ["id_action"],
    )
    op.create_foreign_key(
        "user_action_time_id_user_fkey", "user_action_time", "user", ["id_user"], ["id_user"]
    )
    op.drop_constraint(None, "user_action", type_="foreignkey")
    op.create_foreign_key(
        "user_action_id_user_fkey", "user_action", "user", ["id_user"], ["id_user"]
    )
    op.alter_column("travel", "end_km", existing_type=sa.SMALLINT(), nullable=False)
    op.alter_column("travel", "start_km", existing_type=sa.SMALLINT(), nullable=False)
    op.alter_column(
        "travel", "license_vehicle", existing_type=sa.VARCHAR(length=12), nullable=False
    )
    op.alter_column("travel", "meal_count", existing_type=sa.SMALLINT(), nullable=False)
    op.alter_column("travel", "status", existing_type=sa.VARCHAR(length=50), nullable=False)
    op.alter_column(
        "travel", "end_date", existing_type=sa.DateTime(), type_=sa.DATE(), existing_nullable=False
    )
    op.alter_column(
        "travel",
        "start_date",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.drop_column("travel", "end_municipality")
    op.drop_constraint(None, "action", type_="foreignkey")
    op.create_foreign_key(
        "action_id_project_fkey", "action", "project", ["id_project"], ["id_project"]
    )
