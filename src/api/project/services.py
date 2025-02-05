from enum import Enum

from flask import abort, current_app, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db

from src.api.exception import DBInsertException
from src.models import Project
from .schema import ProjectSchema, ProjectUpdateSchema, ProjectInputSchema


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


def get_project_by_id(project_id : int):
    project_object = db.session.query(Project).filter_by(id_project=project_id).first()
    schema = ProjectSchema()
    project = schema.dump(project_object)
    project['list_action'] = []
    db.session.close()
    return project





def get_all_projects():
    projects = []
    try:
        projects_objects = db.session.query(Project)
        schema = ProjectSchema(many=True)
        projects = schema.dump(projects_objects)
        for project in projects:
                    project['list_action'] = []
        db.session.close()
        return projects
    except ValueError as error:
        current_app.logger.error(f"ProjectDBService - get_all_projects : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()



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
