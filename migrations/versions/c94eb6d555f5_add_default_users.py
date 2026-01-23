"""Add default users

Revision ID: c94eb6d555f5
Revises:
Create Date: 2026-01-14 16:44:03.583914

"""

import csv
import hashlib
import os
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c94eb6d555f5"
down_revision: Union[str, None] = "98959d1da446"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """
    Seed the user table.

    If 'migrations/data/default_users.csv' exists, users from this file
    are inserted.
    Otherwise, a default admin user is created with password 'admin'.
    """
    # Define table structure for bulk insert
    user_table = sa.table(
        "user",
        sa.column("email", sa.String),
        sa.column("first_name", sa.String),
        sa.column("last_name", sa.String),
        sa.column("password", sa.String),
        sa.column("is_admin", sa.Boolean),
    )

    csv_path = "migrations/data/default_users.csv"
    users_to_insert = []

    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                users_to_insert.append(
                    {
                        "email": row["email"],
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "password": row["hashed_password"],
                        "is_admin": row["is_admin"].lower() in ("true", "1", "yes"),
                    }
                )
    else:
        # Create a default admin if CSV is not found
        hashed_password = hashlib.md5("admin".encode("utf-8")).hexdigest()
        users_to_insert.append(
            {
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "GTT",
                "password": hashed_password,
                "is_admin": True,
            }
        )

    if users_to_insert:
        op.bulk_insert(user_table, users_to_insert)

        # Associate all users with actions from project 0
        op.execute(
            """
            INSERT INTO user_action (id_user, id_action)
            SELECT
                u.id_user,
                a.id_action
            FROM "user" AS u
            CROSS JOIN "action" AS a
            WHERE a.id_project = 0
            AND NOT EXISTS (
                SELECT 1
                FROM "user_action" ua
                WHERE ua.id_user = u.id_user
                AND ua.id_action = a.id_action
            );
            """
        )


def downgrade():
    """
    Remove all users from the user table.
    """
    op.execute('DELETE FROM "user_action"')
    op.execute('DELETE FROM "user"')
