import hashlib
from functools import wraps

import requests
from flask import abort, current_app, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from src import api
from src.api import db, user
from src.api.auth.schema import AuthInputSchema
from src.api.exception import MissingFieldError, NotFoundError
from src.config import get_config
from src.models import User

print(hashlib.md5("whatever your string is".encode("utf-8")).hexdigest())


def gtt_auth(data: AuthInputSchema) -> user:
    login = data["login"]
    password = data["password"]
    hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()

    user = (
        db.session.query(User).filter(User.email == login, User.password == hashed_password).first()
    )
    db.session.close()
    if user:
        if user.is_admin:
            role = "admin"
        else:
            role = "user"
        identity = data["login"]

        access_token = create_access_token(
            identity=identity, additional_claims={"role": role, "user_id": user.id_user}
        )
        refresh_token = create_refresh_token(identity=identity)
        return {
            "id_user": user.id_user,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    else:
        raise NotFoundError("No user found for this login/password")


def exchange_code_for_id_token(code, client_id, client_secret, redirect_uri, token_endpoint):
    """
    Exchanges an authorization code for tokens and returns the Google ID token.
    """
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "postmessage",
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_endpoint, data=payload)
    if token_response.status_code != 200:
        current_app.logger.error("Token exchange failed: %s", token_response.text)
        abort(400, description="Failed to exchange authorization code with Google.")
    tokens = token_response.json()
    google_id_token = tokens.get("id_token")
    if not google_id_token:
        abort(400, description="No ID token found in response from Google.")
    return google_id_token


def verify_google_token(google_token, client_id):
    """
    Verifies the Google ID token and returns its payload.
    """
    try:
        idinfo = id_token.verify_oauth2_token(google_token, google_requests.Request(), client_id)
        return idinfo
    except Exception as e:
        abort(400, description="Invalid Google ID token: " + str(e))


def google_auth(data):
    """
    Handles both One Tap (ID token) and Popup (authorization code) flows.

    - If "token" is provided, it verifies that token directly (One Tap flow).
    - If "code" is provided, it exchanges the code for tokens, then verifies the returned ID token (Popup flow).

    After verifying the token, it extracts user info, looks up or creates the user in the database,
    then issues JWT tokens and returns the user data.
    """
    config = get_config()
    client_id = config.GS_CLIENT_ID
    client_secret = config.GS_PRIVATE_KEY
    token_endpoint = config.GS_TOKEN_URI
    redirect_uri = config.GS_AUTH_URI

    # Determine which flow (One Tap vs. Popup)
    if "token" in data:
        # One Tap: directly verify the token
        google_id_token = data["token"]
    elif "code" in data:
        # Popup: exchange code for tokens, then verify
        google_id_token = exchange_code_for_id_token(
            code=data["code"],
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            token_endpoint=token_endpoint,
        )
    else:
        abort(400, description="Missing required field: 'token' or 'code'.")

    # Verify the ID token
    idinfo = verify_google_token(google_id_token, client_id)

    # Extract user info
    email = idinfo.get("email")

    # Look up or create user in DB
    user = db.session.query(User).filter(User.email == email).first()
    db.session.close()
    if user:
        if user.is_admin:
            role = "admin"
        else:
            role = "user"
        identity = user.email

        access_token = create_access_token(
            identity=identity, additional_claims={"role": role, "user_id": user.id_user}
        )
        refresh_token = create_refresh_token(identity=identity)
        return {
            "id_user": user.id_user,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "picture": idinfo.get("picture"),
        }
    else:
        raise NotFoundError("No user found for this login/password")


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
            user_id_from_url = kwargs.get("user_id", None)
            if user_id_from_url is None:
                return {"msg": "User ID is required in the URL."}, 400
            if claims.get("user_id") != user_id_from_url:
                return {
                    "msg": "Forbidden, the connected user does not have the right to access this"
                }, 403
        return fn(*args, **kwargs)

    return wrapper
