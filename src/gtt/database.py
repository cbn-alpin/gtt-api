from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Add naming convention to automatically generate constraint names.
# This is required for Alembic to work correctly.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)


db = SQLAlchemy(metadata=metadata)
