import sqlalchemy
from flask import abort, current_app
from marshmallow import EXCLUDE

from gtt.api.action.schema import ActionSchema
from gtt.api.exception import DBInsertException, DeleteError
from gtt.database import db
from gtt.models import Action, UserActionTime


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
        total_duration = (
            db.session.query(db.func.sum(UserActionTime.duration))
            .join(Action, UserActionTime.id_action == Action.id_action)
            .filter(Action.id_action == action_id)
            .scalar()
        )
        if total_duration and total_duration > 0:
            raise DeleteError(
                f"L'action '{action_id}' ne peut pas être supprimée car "
                "des saisies de temps y sont associées"
            )

        db.session.query(Action).filter_by(id_action=action_id).delete()
        db.session.commit()

        return {"message": f"L'action '{action_id}' a été supprimée avec succès."}
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - delete : {error}")
        raise
