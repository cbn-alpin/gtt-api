from flask import current_app, jsonify,abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from src import api
from src.api import user
from src.api.auth.schema import AuthInputSchema
from src.api.exception import MissingFieldError, NotFoundError
from src.api import db
from src.config import get_config
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
import hashlib


from functools import wraps

from src.models import User
print(hashlib.md5("whatever your string is".encode('utf-8')).hexdigest())


def gtt_auth(data: AuthInputSchema) -> user :
    login = data["login"]
    password = data["password"]
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    user = (
        db.session.query(User).filter(User.email == login, User.password == hashed_password).first()
    )
    db.session.close()
    if user:
        if user.is_admin:
            role = "admin"
        else:
            role = "user"
        identity = data['login']

        access_token = create_access_token(identity=identity, additional_claims={"role": role, "user_id": user.id_user})
        refresh_token = create_refresh_token(identity=identity)
        return {
            'id_user': user.id_user,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    else:
        raise NotFoundError("No user found for this login/password")

def google_auth(data):
    """
    Handles only the popup flow (authorization code) using a mock user.
    Expects 'data' to have a 'code' field.
    """
    config = get_config()
    client_id = config.GS_CLIENT_ID
    client_secret = config.GS_PRIVATE_KEY
    token_endpoint = config.GS_TOKEN_URI
    redirect_uri = config.GS_AUTH_URI 


    if "code" not in data:
        abort(400, description="Missing required field: code")

    code = data["code"]

    # Prepare the payload to exchange the authorization code for tokens
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(token_endpoint, data=payload)
    if token_response.status_code != 200:
        current_app.logger.error("Token exchange failed: %s", token_response.text)
        abort(400, description="Failed to exchange authorization code with Google.")

    tokens = token_response.json()
    google_id_token = tokens.get("id_token")
    if not google_id_token:
        abort(400, description="No ID token found in response from Google.")

    try:
        # Verify the ID token returned by Google
        idinfo = id_token.verify_oauth2_token(google_id_token, google_requests.Request(), client_id)
    except Exception as e:
        abort(400, description="Invalid Google ID token: " + str(e))

    # Extract user info from the verified token
    email = idinfo.get("email")
    given_name = idinfo.get("given_name", "")
    family_name = idinfo.get("family_name", "")

    # Use a mock user for testing purposes
    mock_user = {
        "id_user": "mock456",
        "last_name": family_name,
        "first_name": given_name,
        "email": email,
        "is_admin": False
    }

    role = "admin" if mock_user["is_admin"] else "user"
    identity = email  # Using email as the identity
    access_token = create_access_token(identity=identity, additional_claims={"role": role, "user_id": mock_user["id_user"]})
    refresh_token = create_refresh_token(identity=identity)

    return jsonify({
        'id_user': mock_user["id_user"],
        'last_name': mock_user["last_name"],
        'first_name': mock_user["first_name"],
        'email': mock_user["email"],
        'is_admin': mock_user["is_admin"],
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    # """
    # Handles only the One Tap flow (ID token) using a mock user.
    # Expects 'data' to have a 'token' field.
    # """
    # config = get_config()
    # client_id = config.GS_CLIENT_ID  # Ensure this is correctly set in your config

    # if "token" not in data:
    #     abort(400, description="Missing required field: token")
    
    # google_token = data["token"]
    # try:
    #     # Verify the Google ID token
    #     idinfo = id_token.verify_oauth2_token(google_token, google_requests.Request(), client_id)
    # except Exception as e:
    #     abort(400, description="Invalid Google token: " + str(e))
    
    # # Extract user info from the verified token
    # email = idinfo.get("email")
    # given_name = idinfo.get("given_name", "")
    # family_name = idinfo.get("family_name", "")
    
    # # Use a mock user for testing purposes (since DB isn't accessible right now)
    # mock_user = {
    #     "id_user": "mock123",
    #     "last_name": family_name,
    #     "first_name": given_name,
    #     "email": email,
    #     "is_admin": False  # Adjust as needed
    # }
    
    # # Determine role and identity
    # role = "admin" if mock_user["is_admin"] else "user"
    # identity = email  # Using email as the identity
    
    # # Create JWT tokens using flask_jwt_extended
    # access_token = create_access_token(
    #     identity=identity,
    #     additional_claims={"role": role, "user_id": mock_user["id_user"]}
    # )
    # refresh_token = create_refresh_token(identity=identity)
    
    # # Return a JSON response with mock user info and tokens
    # return jsonify({
    #     'id_user': mock_user["id_user"],
    #     'last_name': mock_user["last_name"],
    #     'first_name': mock_user["first_name"],
    #     'email': mock_user["email"],
    #     'is_admin': mock_user["is_admin"],
    #     'access_token': access_token,
    #     'refresh_token': refresh_token
    # })


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"msg": "Admin access required."}, 403
        return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            user_id_from_url = kwargs.get('user_id', None)
            if user_id_from_url is None:
                return {"msg": "User ID is required in the URL."}, 400
            if claims.get("user_id") != user_id_from_url:
                return {"msg": "Forbidden, the connected user does not have the right to access this"}, 403
        return fn(*args, **kwargs)
    return wrapper
