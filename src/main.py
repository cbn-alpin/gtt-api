# Python libraries

from flask import jsonify
from flask_cors import CORS

from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from src.api import create_api, db
from src.api.project.routes import resources as projects_ressources
from src.api.auth.routes import auth_bp


# Creating the Flask application
api = create_api()

# Database migration
migrate = Migrate(api, db)

CORS(api)

oauth = OAuth(api)

@api.route('/health', methods=['GET'])
def health():
	# Handle here any business logic for ensuring you're application is healthy (DB connections, etc...)
    return "Healthy: OK"


@api.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'status': 'error',
        'type': 'NOT_FOUND',
        'code': 'RESOURCE_NOT_FOUND',
        'message': 'The requested URL was not found on the server. You can check available endpoints at /'
    }), 404

api.register_blueprint(projects_ressources)
api.register_blueprint(auth_bp)
