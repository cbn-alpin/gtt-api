from enum import Enum

from flask import abort, current_app, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db

from src.api.action.schema import ActionSchema
from src.api.exception import DBInsertException
from src.api.project.schema import ProjectSchema, ProjectUpdateSchema, ProjectInputSchema
from src.models import Action, Project


def create_project(data: dict) -> int:
    try:
        project = ProjectInputSchema().load(data)
        project = Project(
            code=project['code'],
            name=project['name'],
            description=project.get('description'),
            start_date=project.get('start_date'),
            end_date=project.get('end_date'),
            is_archived=project.get('is_archived', False)
        )

        db.session.add(project)
        db.session.commit()
        return project.id_project

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()
    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()


def get_project_by_id(project_id: int):
    project_actions = (
        db.session.query(Project, Action)
        .outerjoin(Action, Project.id_project == Action.id_project)
        .filter(Project.id_project == project_id)
        .all()
    )

    project = None
    actions = []

    for project_object, action_object in project_actions:
        if not project:
            project = ProjectSchema().dump(project_object)

        if action_object:
            action = ActionSchema().dump(action_object)
            actions.append(action)

    if actions:
        project['list_action'] = actions
    else:
        project['list_action'] = None

    db.session.close()
    return project





def get_all_projects():
    projects_actions = (
        db.session.query(Project, Action)
        .outerjoin(Action, Project.id_project == Action.id_project)
        .all()
    )

    list_projects = []
    for project_action in projects_actions:
        project_object, action_object = project_action
        project = ProjectSchema().dump(project_object)
        action = ActionSchema().dump(action_object)
        existing_project = next((p for p in list_projects if p["id_project"] == project["id_project"]), None)
        if existing_project:
             existing_project["list_action"].append(action)
        else:
            project["list_action"] = None if not action else [action]
            list_projects.append(project)

    db.session.close()
    return list_projects

def update(project, project_id):
    existing_project = get_project_by_id(project_id)
    if not existing_project:
        abort(404, description="Project not found")
    data = ProjectSchema().load(project, unknown=EXCLUDE)

    db.session.query(Project).filter_by(id_project=project_id).update(data)
    db.session.commit()
    db.session.close()
    return get_project_by_id(project_id)





def delete(project_id: int):
    try:
        db.session.query(Project).filter_by(id_project=project_id).delete()
        db.session.commit()

        db.session.close()
        return {'message': f'Le projet \'{project_id}\' a été supprimé'}
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - delete : {error}")
        raise
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - delete : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()
