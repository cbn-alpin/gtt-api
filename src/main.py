# Python libraries

from flask import jsonify, request
from flask_cors import CORS

from flask_migrate import Migrate
import marshmallow

from src.api import create_api, db, init_db_and_migrations
from src.api.exception import DBInsertException, NotFoundError
from src.api.project.routes import resources as projects_ressources
from src.api.action.routes import resources as actions_ressources
from src.api.user.routes import resources as users_ressources
from src.api.userActionTime.routes import resources as users_action_time_ressources
from src.api.userAction.routes import resources as users_action_ressources
from src.api.auth.routes import resources as auth_ressources
from src.api.travel.routes import resources as travels_ressources



# Creating the Flask application
api = create_api()

# Database migration
init_db_and_migrations(api, db)

# Enable CORS globally for all routes
CORS(api)



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

@api.errorhandler(DBInsertException)
def handle_db_insert_error(error):
    return jsonify({
        'status': 'error',
        'type': 'DATABASE_ERROR',
        'code': 'INSERT_FAILED',
        'message': error.message
    }), error.status_code

@api.errorhandler(NotFoundError)
def handle_db_insert_error(error):
    return jsonify({
        'status': 'error',
        'type': 'NOT_FOUND',
        'code': 'NOT_FOUND',
        'message': error.message
    }), error.status_code

@api.errorhandler(marshmallow.exceptions.ValidationError)
def handle_schema_error(error):
    return jsonify({
        'status': 'error',
        'type': 'DATABASE_ERROR',
        'code': 'INSERT_FAILED',
        'message': "error, schema incorrect"
    }), 400


api.register_blueprint(projects_ressources)
api.register_blueprint(users_ressources)
api.register_blueprint(users_action_time_ressources)
api.register_blueprint(users_action_ressources)
api.register_blueprint(actions_ressources)
api.register_blueprint(auth_ressources)
api.register_blueprint(travels_ressources)
