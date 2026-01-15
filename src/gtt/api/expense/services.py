import sqlalchemy
from flask import current_app

from gtt.api.exception import DBInsertException
from gtt.api.expense.schema import ExpensePostSchema, ExpenseTravelSchema
from gtt.database import db
from gtt.models import Expense


def create_expense(expense: dict, travel_id: int) -> int:
    try:
        expense = ExpensePostSchema().load(expense)
        new_expense = Expense(
            name=expense["name"],
            comment=expense.get("comment"),
            amount=expense.get("amount"),
            id_travel=travel_id,
        )

        db.session.add(new_expense)
        db.session.commit()
        return new_expense.id_expense

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ExpenseDBService - insert : {error}")
        raise DBInsertException() from error

    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"ExpenseDBService - insert : {error}")
        raise DBInsertException() from error


def get_expense_by_id(expense_id: int):
    action_object = db.session.query(Expense).filter(Expense.id_expense == expense_id).first()
    schema = ExpenseTravelSchema()
    action = schema.dump(action_object)
    return action


def update(expense_data, expense_id):
    data = ExpensePostSchema().load(expense_data)
    db.session.query(Expense).filter_by(id_expense=expense_id).update(data)
    db.session.commit()
    return get_expense_by_id(expense_id)


def delete(expense_id: int):
    try:
        db.session.query(Expense).filter_by(id_expense=expense_id).delete()
        db.session.commit()
        return {"message": f"La note du frais '{expense_id}' a été supprimé"}
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ProjectDBService - delete : {error}")
        raise
