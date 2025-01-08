from flask import request, jsonify
from app import app, db
from models import User 

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if data.get('email') and data.get('first_name') and data.get('last_name'):
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=data.get('is_admin', False),
            password=data['password']
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created', 'user': user.id_user}), 201
    else:
        return jsonify({'message': 'Missing required fields'}), 400

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id_user': user.id_user,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_admin': user.is_admin
    } for user in users])

# Get a user by ID
@app.route('/users/<int:id_user>', methods=['GET'])
def get_user(id_user):
    user = User.query.get(id_user)
    if user:
        return jsonify({
            'id_user': user.id_user,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin
        })
    return jsonify({'message': f'User with ID {id_user} not found'}), 404

# Update a user by ID
@app.route('/users/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    user = User.query.get(id_user)
    if user:
        data = request.get_json()
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.is_admin = data.get('is_admin', user.is_admin)
        user.password = data.get('password', user.password)

        db.session.commit()

        return jsonify({'message': 'User updated'})
    return jsonify({'message': f'User with ID {id_user} not found'}), 404

# Delete a user by ID
@app.route('/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    user = User.query.get(id_user)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'})
    return jsonify({'message': f'User with ID {id_user} not found'}), 404
