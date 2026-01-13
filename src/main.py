import marshmallow
from flask import Flask, jsonify
from flask_cors import CORS

from src.api.action.routes import resources as actions_ressources
from src.api.auth.routes import resources as auth_ressources
from src.api.exception import DBInsertException, NotFoundError
from src.api.expense.routes import resources as expenses_ressources
from src.api.project.routes import resources as projects_ressources
from src.api.travel.routes import resources as travels_ressources
from src.api.user.routes import resources as users_ressources
from src.api.userAction.routes import resources as users_action_ressources
from src.api.userActionTime.routes import resources as users_action_time_ressources
from src.config import get_config
from src.database import db
from src.extensions import jwt


def create_api(config_overrides: dict = None):
    """
    Create API with Flask.
    """
    app = Flask(__name__, template_folder="templates")

    if config_overrides:
        app.config.from_mapping(config_overrides)
    else:
        config = get_config()
        app.config["SQLALCHEMY_DATABASE_URI"] = config.get_engine_uri()
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = config.SQLALCHEMY_ENGINE_OPTIONS
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
        app.config["JWT_SECRET_KEY"] = config.JWT_SECRET
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_EXPIRES_IN
        app.config["JWT_BLACKLIST_ENABLED"] = config.JWT_BLACKLIST_ENABLED
        app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = config.JWT_BLACKLIST_TOKEN_CHECKS

    jwt.init_app(app)
    db.init_app(app)

    # Enable CORS globally for all routes
    CORS(app)

    app.register_blueprint(projects_ressources, url_prefix="/api")
    app.register_blueprint(users_ressources, url_prefix="/api")
    app.register_blueprint(users_action_time_ressources, url_prefix="/api")
    app.register_blueprint(users_action_ressources, url_prefix="/api")
    app.register_blueprint(actions_ressources, url_prefix="/api")
    app.register_blueprint(auth_ressources, url_prefix="/api")
    app.register_blueprint(travels_ressources, url_prefix="/api")
    app.register_blueprint(expenses_ressources, url_prefix="/api")
    return app


# Creating the Flask application
api = create_api()

@api.route("/health", methods=["GET"])
def health():
    return "Healthy: OK"


@api.errorhandler(404)
def page_not_found(e):
    return (
        jsonify(
            {
                "status": "error",
                "type": "NOT_FOUND",
                "code": "RESOURCE_NOT_FOUND",
                "message": (
                    "The requested URL was not found on the server. "
                    "You can check available endpoints at /"
                ),
            }
        ),
        404,
    )


@api.errorhandler(DBInsertException)
def handle_db_insert_error(error):
    return (
        jsonify(
            {
                "status": "error",
                "type": "DATABASE_ERROR",
                "code": "INSERT_FAILED",
                "message": error.message,
            }
        ),
        error.status_code,
    )


@api.errorhandler(NotFoundError)
def handle_db_not_found_error(error):
    return (
        jsonify(
            {
                "status": "error",
                "type": "NOT_FOUND",
                "code": "NOT_FOUND",
                "message": error.message,
            }
        ),
        error.status_code,
    )


@api.errorhandler(marshmallow.exceptions.ValidationError)
def handle_schema_error(error):
    return (
        jsonify(
            {
                "status": "error",
                "type": "DATABASE_ERROR",
                "code": "INSERT_FAILED",
                "message": "error, schema incorrect",
            }
        ),
        400,
    )
