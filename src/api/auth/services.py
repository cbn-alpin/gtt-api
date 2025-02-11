import os
import datetime
import jwt
import google.auth.transport.requests
import google.oauth2.id_token
from flask import request, jsonify
from src.config import get_config

config = get_config()

GS_CLIENT_ID = config.GS_CLIENT_ID
JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = 'HS256'

def create_app_token(user_info):
    """
    Generate an application-specific JWT token using information from the verified Google token.
    """
    payload = {
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    # token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # if isinstance(token, bytes):
    #     token = token.decode('utf-8')
    return payload

def google_auth():
    """
    Verifies the Google JWT received from the client and returns an application-specific token.
    """
    data = request.get_json()
    google_token = data.get('token')
    if not google_token:
        return jsonify({'error': 'Token missing'}), 400

    try:
        # Create a request adapter for verifying the token.
        request_adapter = google.auth.transport.requests.Request()
        # Verify the Google token. This function checks the token's signature, expiration, and audience.
        id_info = google.oauth2.id_token.verify_oauth2_token(
            google_token, request_adapter, GS_CLIENT_ID
        )

        # Once verified, generate an application-specific token.
        app_token = create_app_token(id_info)
        return jsonify({'token': app_token})

    except ValueError as e:

        return jsonify({'error': 'Invalid token', 'message': str(e)}), 401
