from flask import Blueprint, current_app, request, jsonify, abort
from src.api.project.services import ProjectDBService
from src.models import Project



resources = Blueprint('projects', __name__)


# Create a new project
@resources.route('/api/projects', methods=['POST'])
def create_project():
    posted_data = request.get_json()

    current_app.logger.debug('In POST /api/projects')
    response = None
    try:
        posted_data = request.get_json()
        response = ProjectDBService.insert(posted_data)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'Une erreur est survenue lors de l\'enregistrement du projet'}), 500
    finally:
        return response



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
