from datetime import datetime
from flask import Blueprint, current_app, request, jsonify, abort
from src.api.auth.services import user_required
from src.api.travel.services import create_travel

resources = Blueprint('travels', __name__)


# Create a new travel
@resources.route('/api/user/<int:user_id>/project/<int:project_id>/travels/', methods=['POST'])
@user_required
def post_travel(user_id:int, project_id:int):
    data = request.get_json()

    current_app.logger.debug('In POST /api/user/<int:user_id>/project/<int:project_id>/travels/')
    if data.get('start_date') and data.get('end_date'):
        try:
            if datetime.strptime(data.get('start_date'), "%Y-%m-%d") > datetime.strptime(data.get('end_date'), "%Y-%m-%d"):
                abort(400, description="Start date after end date")
        except ValueError:
            abort(400, description="Invalid date format")

    travel_id = create_travel(user_id, project_id, data)
    return jsonify({'message': 'Travel created', 'travel_id': travel_id}), 201

