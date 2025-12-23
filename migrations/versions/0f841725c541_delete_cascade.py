"""delete cascade

Revision ID: 0f841725c541
Revises: 93af8d60f524
Create Date: 2025-02-06 08:08:22.279505

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0f841725c541"
down_revision: Union[str, None] = "93af8d60f524"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("user_action_id_action_fkey", "user_action", type_="foreignkey")
    op.create_foreign_key(
        None, "user_action", "action", ["id_action"], ["id_action"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(None, "user_action", type_="foreignkey")
    op.create_foreign_key(
        "user_action_id_action_fkey", "user_action", "action", ["id_action"], ["id_action"]
    )
