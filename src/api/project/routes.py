from flask import Blueprint, request, jsonify, abort
from src.api.project.services import create_project
from src.models import Project

resources = Blueprint('projects', __name__)


# Create a new project
@resources.route('/projects', methods=['POST'])
def post_project():
    data = request.get_json()

    if not data.get('code') or not data.get('name'):
        abort(400, description="Code and Name are required fields")

    project_id = create_project(data)

    return jsonify({'message': 'Project created', 'project': project_id}), 201
