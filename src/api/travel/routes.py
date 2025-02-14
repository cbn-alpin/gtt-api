from datetime import datetime
from flask import Blueprint, current_app, request, jsonify, abort
from src.api.travel.services import get_travel_by_id, update
from src.api.auth.services import user_required
from src.api.travel.services import create_travel

resources = Blueprint('travels', __name__)


# Create a new travel
@resources.route('/api/travels/user/<int:user_id>/project/<int:project_id>', methods=['POST'])
@user_required
def post_travel(user_id:int, project_id:int):
    data = request.get_json()

    current_app.logger.debug('In POST /api/travels/user/<int:user_id>/project/<int:project_id>')
    if data.get('start_date') and data.get('end_date'):
        try:
            if datetime.strptime(data.get('start_date'), "%Y-%m-%d") > datetime.strptime(data.get('end_date'), "%Y-%m-%d"):
                abort(400, description="Start date after end date")
        except ValueError:
            abort(400, description="Invalid date format")

    travel_id = create_travel(user_id, project_id, data)
    return jsonify({'message': 'Travel created', 'travel_id': travel_id}), 201

   
@resources.route('/api/travels/<int:travel_id>/user/<int:user_id>', methods=['PUT'])
@user_required 
def update_travel(travel_id: int, user_id: int):
    existing_travel = get_travel_by_id(travel_id)
    print(existing_travel)
    if not existing_travel:  
        abort(404, description="Travel not found")
    if existing_travel.get('id_user') != user_id:  
        abort(403, description="Unauthorized to update this travel")
    current_app.logger.info(f'In PUT /api/travels/<int:travel_id>')
    posted_data = request.get_json()
    response = update(posted_data, travel_id)
    response = jsonify(response), 200
    return response