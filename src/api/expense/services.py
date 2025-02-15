from flask import current_app
import sqlalchemy
from src.api import db
from src.api.exception import DBInsertException
from src.api.expense.schema import ExpensePostSchema, ExpenseSchema
from src.models import Expense

def create_expense(expense: dict) -> int:
    try:
        expense = ExpensePostSchema().load(expense)
        new_expense = Expense(
            name=expense['name'],
            comment=expense.get('comment'),
            amount=expense.get('amount'),
            id_travel=expense.get('id_travel')
        )

        db.session.add(new_expense)
        db.session.commit()
        return new_expense.id_expense

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"ExpenseDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()

    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"ExpenseDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()