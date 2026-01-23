"""add_default_projects

Revision ID: 3e092233071d
Revises:  e1e4cccc9eb3
Create Date: 2026-01-23 16:38:33.580308

"""
import os
import csv
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '3e092233071d'
down_revision: Union[str, None] = 'e1e4cccc9eb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Seed the project table.

    If 'migrations/data/default_projects.csv' exists, projects from this file
    are inserted.
    Otherwise, a default project "0" is created.
    """
    # Define table structure for bulk insert
    project_table = sa.table(
        "project",
        sa.column("id_project", sa.String),
        sa.column("code", sa.String),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
        sa.column("start_date", sa.Date),
        sa.column("end_date", sa.Date),
        sa.column("is_archived", sa.Boolean),
    )

    csv_path = "migrations/data/default_projects.csv"
    projects_to_insert = []

    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            id_project = 0
            for row in reader:
                projects_to_insert.append(
                    {
                        "id_project": id_project,
                        "code": row["code"],
                        "name": row["name"],
                        "description": row.get("description", None),
                        "start_date": row["start_date"],
                        "end_date": row.get("end_date", None),
                        "is_archived": row.get("is_archived", "false").lower() in ("true", "1", "yes"),
                    }
                )
                id_project += 1
    else:
        # Create a default project if CSV is not found
        projects_to_insert.append(
            {
                "id_project": 0,
                "code": "DEFAULT",
                "name": "Default Project",
                "description": "Default project for GTT.",
                "start_date": datetime.today().strftime('%Y-%m-%d'),
                "end_date": None,
                "is_archived": False,
            }
        )

    if projects_to_insert:
        op.bulk_insert(project_table, projects_to_insert)


def downgrade():
    """
    Remove all projects from the project table.
    """
    op.execute('DELETE FROM "project"')
