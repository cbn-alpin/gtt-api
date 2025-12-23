"""add delete cascade to travel

Revision ID: e1e4cccc9eb3
Revises: 43c8214be822
Create Date: 2025-02-16 10:41:55.593854

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1e4cccc9eb3"
down_revision: Union[str, None] = "43c8214be822"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("expense_id_travel_fkey", "expense", type_="foreignkey")
    op.create_foreign_key(
        None, "expense", "travel", ["id_travel"], ["id_travel"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(None, "expense", type_="foreignkey")
    op.create_foreign_key(
        "expense_id_travel_fkey", "expense", "travel", ["id_travel"], ["id_travel"]
    )
