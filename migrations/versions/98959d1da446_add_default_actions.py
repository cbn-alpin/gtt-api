"""add_default_actions

Revision ID: 98959d1da446
Revises: 3e092233071d
Create Date: 2026-01-23 17:01:01.196694

"""
from typing import Sequence, Union
import os
import csv

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98959d1da446'
down_revision: Union[str, None] = '3e092233071d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Seed the action table.

    If 'migrations/data/default_actions.csv' exists, actions from this file
    are inserted.
    Otherwise, a default action "0" is created.
    """
    # Define table structure for bulk insert
    action_table = sa.table(
        "action",
        sa.column("numero_action", sa.String), # Corrected column name
        sa.column("name", sa.String),
        sa.column("description", sa.String),
        sa.column("id_project", sa.Integer),
    )

    # Define project table structure to query id_project
    project_table = sa.table(
        "project",
        sa.column("id_project", sa.Integer),
        sa.column("code", sa.String),
    )

    csv_path = "migrations/data/default_actions.csv"
    actions_to_insert = []

    connection = op.get_bind()
    projects_map = {}

    # Fetch all projects to create a lookup map (code -> id_project)
    # This is more efficient than querying inside the loop for each action
    result = connection.execute(sa.select(project_table.c.id_project, project_table.c.code))
    for id_project, code in result:
        projects_map[code] = id_project

    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                actions_to_insert.append(
                    {
                        "numero_action": row["numero"],
                        "name": row["name"],
                        "description": row.get("description", None),
                        "id_project": projects_map.get(row["code_project"], 0),
                    }
                )
    else:
        # Create a default actions if CSV is not found
        default_project_id = projects_map.get("DEFAULT", 0)
        actions_to_insert.append(
            {
                "numero_action": "0",
                "name": "Default Action",
                "description": "Default action for GTT.",
                "id_project": default_project_id,
            }
        )

    if actions_to_insert:
        op.bulk_insert(action_table, actions_to_insert)


def downgrade() -> None:
    """
    Remove all actions from the action table.
    """
    op.execute('DELETE FROM "action"')