from flask import request, jsonify, abort
from app import app, db
from models import Project

# Create a new project
@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()

    if not data.get('code') or not data.get('name'):
        abort(400, description="Code and Name are required fields")

    project = Project(
        code=data['code'],
        name=data['name'],
        description=data.get('description'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        is_archived=data.get('is_archived', False)
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Project created', 'project': project.id_project}), 201

# Get all projects
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id_project': project.id_project,
        'code': project.code,
        'name': project.name,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'is_archived': project.is_archived
    } for project in projects])

# Get a project by ID
@app.route('/projects/<int:id_project>', methods=['GET'])
def get_project(id_project):
    project = Project.query.get(id_project)

    return jsonify({
        'id_project': project.id_project,
        'code': project.code,
        'name': project.name,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'is_archived': project.is_archived
    })

# Update a project by ID
@app.route('/projects/<int:id_project>', methods=['PUT'])
def update_project(id_project):
    project = Project.query.get(id_project)

    data = request.get_json()
    project.code = data.get('code', project.code)
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.start_date = data.get('start_date', project.start_date)
    project.end_date = data.get('end_date', project.end_date)
    project.is_archived = data.get('is_archived', project.is_archived)

    db.session.commit()

    return jsonify({'message': 'Project updated'})

# Delete a project by ID
@app.route('/projects/<int:id_project>', methods=['DELETE'])
def delete_project(id_project):
    project = Project.query.get(id_project)

    db.session.delete(project)
    db.session.commit()

    return jsonify({'message': 'Project deleted'})
