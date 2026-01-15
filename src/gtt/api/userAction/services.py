from flask import current_app
from sqlalchemy.exc import IntegrityError

from gtt.api.exception import DBInsertException
from gtt.database import db
from gtt.models import UserAction


def create_user_action(user_id: int, action_id: int) -> dict:
    """Create a new user action."""
    try:
        user_action = UserAction(id_user=user_id, id_action=action_id)
        db.session.add(user_action)
        db.session.commit()
        return {"id_user": user_action.id_user, "id_action": user_action.id_action}
    except IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"UserActionService - create : {error}")
        raise DBInsertException() from error
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"UserActionService - create : {error}")
        raise error


def delete_user_action_service(user_id: int, action_id: int):
    """Delete a user action."""
    user_action = (
        db.session.query(UserAction).filter_by(id_user=user_id, id_action=action_id).first()
    )
    if not user_action:
        raise ValueError("User action not found")

    db.session.delete(user_action)
    db.session.commit()
    return {"message": f"User {user_id} action {action_id} deleted successfully"}
