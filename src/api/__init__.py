from os import environ

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from src.config import get_config

__version__ = "0.1.0"

db = SQLAlchemy()
jwt = JWTManager()


def init_db_and_migrations(app, db):
    try:
        # First check if we can connect to the database
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            db.session.commit()
    except Exception as e:
        app.logger.warning(f"Database connection failed: {e}")
        return False

    try:
        # Get Alembic configuration
        alembic_cfg = Config(toml_file="pyproject.toml")

        with app.app_context():
            # Create a connection from the engine
            with db.engine.connect() as connection:
                # Check current database version
                context = MigrationContext.configure(
                    connection
                )  # Using connection instead of engine
                current_rev = context.get_current_revision()

                if current_rev is None:
                    app.logger.info("No previous migrations found. Running all migrations...")
                    command.upgrade(alembic_cfg, "head")
                    return True
                else:
                    # Check if there are any pending migrations
                    script = command.ScriptDirectory.from_config(alembic_cfg)
                    head_rev = script.get_current_head()

                    if current_rev != head_rev:
                        app.logger.info(
                            f"Database needs upgrade. Current: {current_rev}, Head: {head_rev}"
                        )
                        command.upgrade(alembic_cfg, "head")
                        return True
                    else:
                        app.logger.info("Database is up to date")
                        return False

    except Exception as e:
        app.logger.error(f"Migration failed: {e}")
        raise


def create_api(env: str = "development"):
    """
    Create API with Flask.
    """
    env = environ.get("FLASK_ENV", env)
    config = get_config()
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get_engine_uri()
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(config.JWT_EXPIRES_IN)
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

    jwt.init_app(app)
    db.init_app(app)
    return app
