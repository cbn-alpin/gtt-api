from flask import current_app
from sqlalchemy.exc import IntegrityError
from src.api import db
from src.models import UserAction
from src.api.exception import DBInsertException

def create_user_action(data: dict) -> int:
    """Create a new user action."""
    try:
        user_action = UserAction(
            id_user=data['user_id'],
            id_action=data['action_id']
        )
        db.session.add(user_action)
        db.session.commit()
        return user_action.id_user  # Return the user action ID (or any relevant ID)
    except IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"UserActionService - create : {error}")
        raise DBInsertException()
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"UserActionService - create : {error}")
        raise error

def delete_user_action_service(user_action_id: int):
    """Delete a user action."""
    user_action = db.session.query(UserAction).filter_by(id_user=user_action_id).first()
    if not user_action:
        raise ValueError("User action not found")

    db.session.delete(user_action)
    db.session.commit()
    return {'message': f'User action {user_action_id} deleted successfully'}
