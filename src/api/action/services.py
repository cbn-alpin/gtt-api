from flask import abort, current_app
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db
from src.api.action.schema import ActionSchema
from src.api.exception import DBInsertException
from src.api.project.schema import ProjectSchema
from src.models import Action, Project

def create_action(action: dict) -> int:
    try:
        new_action = Action(
            name=action['name'],
            description=action.get('description'),
            id_project=action.get('id_project')
        )

        db.session.add(new_action)
        db.session.commit()
        return new_action.id_action

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ActionDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()

    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"ActionDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()
    
