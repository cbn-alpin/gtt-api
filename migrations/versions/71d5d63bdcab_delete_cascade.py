"""delete cascade

Revision ID: 71d5d63bdcab
Revises: 8d2905c4c6bc
Create Date: 2025-02-06 08:19:54.437514

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "71d5d63bdcab"
down_revision: Union[str, None] = "0f841725c541"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
