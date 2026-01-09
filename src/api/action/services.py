import sqlalchemy
from flask import abort, current_app
from marshmallow import EXCLUDE

from src.api.action.schema import ActionSchema
from src.api.exception import DBInsertException
from src.database import db
from src.models import Action


def create_action(action: dict) -> int:
    try:
        new_action = Action(
            name=action["name"],
            numero_action=action.get("numero_action"),
            description=action.get("description"),
            id_project=action.get("id_project"),
        )
        db.session.add(new_action)
        db.session.commit()
        return new_action.id_action
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ActionDBService - insert : {error}")
        raise DBInsertException() from error
    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"ActionDBService - insert : {error}")
        raise DBInsertException() from error


def get_action_by_id(action_id: int):
    action_object = db.session.query(Action).filter(Action.id_action == action_id).first()
    schema = ActionSchema()
    action = schema.dump(action_object)
    return action


def update(action, action_id):
    existing_action = get_action_by_id(action_id)
    if not existing_action:
        abort(404, description="Action not found")
    data = ActionSchema().load(action, unknown=EXCLUDE)
    db.session.query(Action).filter_by(id_action=action_id).update(data)
    db.session.commit()
    return get_action_by_id(action_id)


def delete(action_id: int):
    try:
        db.session.query(Action).filter_by(id_action=action_id).delete()
        db.session.commit()

        return {"message": f"Le projet '{action_id}' a été supprimé"}
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - delete : {error}")
        raise
