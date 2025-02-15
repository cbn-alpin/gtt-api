from flask import Blueprint, current_app, request, jsonify, abort
from src.api.auth.services import user_required
from src.api.expense.services import create_expense

resources = Blueprint('expenses', __name__)


# Create a new expense
@resources.route('/api/expenses', methods=['POST'])
def post_expense():
    data = request.get_json()

    current_app.logger.debug('In POST /api/expenses')
    if not data.get('name'):
        abort(400, description="name field is missing")

    expense_id = create_expense(data)
    return jsonify({'message': 'Expense created', 'expense_id': expense_id}), 201
