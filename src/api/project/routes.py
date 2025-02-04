from datetime import datetime
from flask import Blueprint, current_app, request, jsonify, abort
from src.api.project.services import ProjectDBService, create_project
from src.models import Project

resources = Blueprint('projects', __name__)


# Create a new project
@resources.route('/api/projects', methods=['POST'])
def post_project():
    data = request.get_json()

    current_app.logger.debug('In POST /api/projects')
    if not data.get('code') or not data.get('name'):
        abort(400, description="Code and Name are required fields")

    if data.get('start_date') and data.get('end_date'):
        try:
            if datetime.strptime(data.get('start_date'), "%Y-%m-%d") > datetime.strptime(data.get('end_date'), "%Y-%m-%d"):
                abort(400, description="Start date after end date")
        except ValueError:
            abort(400, description="Invalid date format")

    project_id = create_project(data)
    return jsonify({'message': 'Project created', 'project': project_id}), 201


# Get all projects
@resources.route('/api/projects', methods=['GET'])
def get_projects():
    current_app.logger.info('In GET /api/projects')
    response = None
    try:
        response = ProjectDBService.get_all_projects()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la récupération des données projets'}), 500
    finally:
        return response




@resources.route('/api/projects/{project_id}', methods=['PUT'])
def update_project(project_id: int):

    current_app.logger.info(f'In PUT /api/projects/{project_id}')

    response = None
    try:
        posted_data = request.get_data
        response = ProjectDBService.update(posted_data)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la modification des données du projet'}), 500
    finally:
        return response




@resources.route('/api/projects/{project_id}', methods=['PUT'])
def delete_project(project_id: int):
    current_app.logger.info('In DELETE /api/projects/{project_id}')
    try:
        project = ProjectDBService.get_project_by_id(project_id)
        response = ProjectDBService.delete(project_id, project['name'])
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de la suppression du projet'}), 500
    finally:
        return response
