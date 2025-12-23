"""add delete cascade to travel

Revision ID: 43c8214be822
Revises: 0d48814d71a9
Create Date: 2025-02-16 10:37:20.642921

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "43c8214be822"
down_revision: Union[str, None] = "0d48814d71a9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "travel",
        "night_municipality",
        existing_type=sa.VARCHAR(length=50),
        nullable=True,
        existing_server_default=sa.text("'sisteron'::character varying"),
    )


def downgrade() -> None:
    op.alter_column(
        "travel",
        "night_municipality",
        existing_type=sa.VARCHAR(length=50),
        nullable=False,
        existing_server_default=sa.text("'sisteron'::character varying"),
    )
