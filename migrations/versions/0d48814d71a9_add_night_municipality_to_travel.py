"""add night_municipality to travel

Revision ID: 0d48814d71a9
Revises: 2076792f348d
Create Date: 2025-02-16 09:24:22.093999

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0d48814d71a9"
down_revision: Union[str, None] = "2076792f348d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "travel",
        sa.Column(
            "night_municipality", sa.String(length=50), nullable=False, server_default="sisteron"
        ),
    )


def downgrade() -> None:
    op.drop_column("travel", "night_municipality")
