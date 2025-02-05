from enum import Enum

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db

from src.api.exception import DBInsertException
from src.models import Project
from .schema import ProjectInputSchema, ProjectSchema


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



def get_all_projects():
    projects = []
    try:
        projects_objects = db.session.query(Project)

        schema = ProjectSchema(many=True)
        projects = schema.dump(projects_objects)

        db.session.close()
        return projects
    except ValueError as error:
        current_app.logger.error(f"ProjectDBService - get_all_projects : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()



def update(project):
    update_project = None
    try:
        data = ProjectSchema(only=('code', 'name', 'description', 'start_date', 'end_date')) \
            .load(project, unknown=EXCLUDE)
        project = Project(**data)

        db.session.merge(project)
        db.session.commit()

        update_project = ProjectSchema().dump(project)
        db.session.close()
        return update_project
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - update : {error}")
        raise
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - update : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()



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
