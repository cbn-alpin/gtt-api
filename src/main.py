# Python libraries

from flask import jsonify

from flask_migrate import Migrate

from src.api import create_api, db

# Creating the Flask application
api = create_api()

# Database migration
migrate = Migrate(api, db)




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

