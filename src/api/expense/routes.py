from flask import Blueprint, current_app, request, jsonify, abort
from src.api.auth.services import user_required
from src.api.expense.services import create_expense, get_expense_by_id, update
from src.api.travel.services import get_travel_by_id

resources = Blueprint('expenses', __name__)


# Create a new expense
@resources.route('/api/expenses/user/<int:user_id>/travel/<int:travel_id>', methods=['POST'])
@user_required
def post_expense(travel_id:int, user_id:int):
    data = request.get_json()

    existing_travel = get_travel_by_id(travel_id)
    if not existing_travel:
        abort(404, description="Associated travel not found")

    if existing_travel.get('id_user') != user_id:
        abort(403, description="Unauthorized to update this expense")

    current_app.logger.debug('In POST /api/expenses')
    if not data.get('name'):
        abort(400, description="name field is missing")

    expense_id = create_expense(data, travel_id)
    return jsonify({'message': 'Expense created', 'expense_id': expense_id}), 201


@resources.route('/api/expenses/<int:expense_id>/user/<int:user_id>', methods=['PUT'])
@user_required
def update_expense(expense_id: int, user_id: int):
    existing_expense = get_expense_by_id(expense_id)
    if not existing_expense:
        abort(404, description="Expense not found")

    existing_travel = get_travel_by_id(existing_expense.get('id_travel'))
    if not existing_travel:
        abort(404, description="Associated travel not found")

    if existing_travel.get('id_user') != user_id:
        abort(403, description="Unauthorized to update this expense")

    current_app.logger.info(f'In PUT /api/expenses/<int:expense_id>/user/<int:user_id>')
    posted_data = request.get_json()
    response = update(posted_data, expense_id)
    response = jsonify(response), 200
    return response