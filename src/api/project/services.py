from enum import Enum

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
from src.api import db
from sqlalchemy import or_
from sqlalchemy.orm import subqueryload

from src.models import Project
from .schema import ProjectSchema

Session = SQLAlchemy().session

def create_project(project: dict) -> int:
    try:
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
        raise
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - insert : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()

class ProjectDBService:
    @staticmethod
    def insert(project):
        session = None
        new_project = None
        try:
            posted_project = ProjectSchema(only=('code', 'name', 'description', 'start_date', 'end_date', 'is_archived', 'list_action')).load(project, unknown=EXCLUDE)
            project = Project(**posted_project)

            # Start DB session
            session = Session()
            session.add(project)
            session.commit()

            new_project = ProjectSchema().dump(project)
            session.close()
            return new_project
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ProjectDBService - insert : {error}")
            raise
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ProjectDBService - insert : {error}")
            raise
        finally:
            if session is not None:
                session.close()



    @staticmethod
    def get_all_projects():
        session = None
        projects = []
        try:
            session = Session()
            projects_objects = session.query(Project)

            # Transforming into JSON-serializable objects
            schema = ProjectSchema(many=True)
            projects = schema.dump(projects_objects)

            # Serializing as JSON
            session.close()
            return projects
        except Exception as error:
            current_app.logger.error(f"ProjectDBService - get_all_projects : {error}")
            raise
        except ValueError as error:
            current_app.logger.error(f"ProjectDBService - get_all_projects : {error}")
            raise
        finally:
            if session is not None:
                session.close()



    @staticmethod
    def update(project):
        session = None
        update_project = None
        try:
            data = ProjectSchema(only=('code', 'name', 'description', 'start_date', 'end_date')) \
                .load(project, unknown=EXCLUDE)
            project = Project(**data)

            session = Session()
            session.merge(project)
            session.commit()

            update_project = ProjectSchema().dump(project)
            session.close()
            return update_project
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ProjectDBService - update : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ProjectDBService - update : {error}")
            raise
        finally:
            if session is not None:
                session.close()


    @staticmethod
    def delete(project_id: int, name: str):
        session = None
        try:
            session = Session()
            session.query(Project).filter_by(id_project=project_id).delete()
            session.commit()

            session.close()
            return {'message': 'Le projet \'{}\' a été supprimé'.format(name)}
        except Exception as error:
            session.rollback()
            current_app.logger.error(f"ProjectDBService - delete : {error}")
            raise
        except ValueError as error:
            session.rollback()
            current_app.logger.error(f"ProjectDBService - delete : {error}")
            raise
        finally:
            if session is not None:
                session.close()
