from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    db.init_app(app)
    return app
