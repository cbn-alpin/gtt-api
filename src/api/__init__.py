from os import environ

from flask import Flask
from flask_jwt_extended import JWTManager

from src.config import get_config

__version__ = "0.1.0"

jwt = JWTManager()




def create_api(env: str = "development"):
    """
    Create API with Flask.
    """
    env = environ.get("FLASK_ENV", env)
    config = get_config()
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get_engine_uri()
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = config.SQLALCHEMY_ENGINE_OPTIONS
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_EXPIRES_IN
    app.config["JWT_BLACKLIST_ENABLED"] = config.JWT_BLACKLIST_ENABLED
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = config.JWT_BLACKLIST_TOKEN_CHECKS

    jwt.init_app(app)
    db.init_app(app)
    return app
