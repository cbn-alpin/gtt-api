from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.api.auth.routes import init_oauth
from src.config import get_config

__version__ = '0.1.0'

db = SQLAlchemy()

def create_api(env: str='dev'):
    """
    Create API with Flask.
    """
    config = get_config()
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_engine_uri(env)

    app.config["SECRET_KEY"] = config.JWT_SECRET
    app.config["SESSION_COOKIE_NAME"] = "flask_session"
    app.config["SESSION_COOKIE_HTTPONLY"] = True  # Protect against XSS attacks
    app.config["SESSION_COOKIE_SECURE"] = False  # Set to True if using HTTPS
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    db.init_app(app)

    with app.app_context():
        init_oauth()
        
    return app
