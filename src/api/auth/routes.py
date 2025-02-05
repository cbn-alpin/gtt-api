from flask import Blueprint, redirect, request, jsonify, current_app
from datetime import datetime, timedelta
import os
from src.api.auth.utils import generate_jwt
from authlib.integrations.flask_client import OAuth

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()  # Lazy initialization (no app passed yet)

def init_oauth():
    """This function will be called later in `main.py` after the app is created."""
    oauth.init_app(current_app)  # Attach OAuth to the app

    authentik_authorize_url = os.getenv("AUTHENTIK_AUTHORIZE_URL", "https://auth.cbna.com/application/o/authorize/")
    google_authorize_url = os.getenv("GS_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")


    if not authentik_authorize_url or not google_authorize_url:
        raise RuntimeError("Missing 'authorize_url' value. Ensure AUTHENTIK_AUTHORIZE_URL and GS_AUTH_URI are set.")

    oauth.register(
        name="authentik",
        client_id=os.getenv("AUTHENTIK_CLIENT_ID"),
        client_secret=os.getenv("GS_PRIVATE_KEY"),
        access_token_url="https://auth.cbna.com/application/o/token/",
        authorize_url="https://auth.cbna.com/application/o/authorize/",
        client_kwargs={"scope": "openid profile email"},
    )

    oauth.register(
        name="google",
        client_id=os.getenv("GS_CLIENT_ID"),
        client_secret=os.getenv("GS_PRIVATE_KEY"),
        access_token_url=os.getenv("GS_TOKEN_URI"),
        authorize_url=os.getenv("GS_AUTH_URI"),
        client_kwargs={"scope": "openid profile email"},
    )

@auth_bp.route("/auth/login-authentik")
def login_authentik():
    return oauth.authentik.authorize_redirect("http://localhost:5000/auth/callback/authentik")

@auth_bp.route("/auth/google/login")
def login_google():
    return oauth.google.authorize_redirect("http://localhost:5000/auth/callback/google")

@auth_bp.route("/auth/callback/<provider>")
def auth_callback(provider):
    """Handles OAuth callback for both Google & Authentik."""
    if provider not in oauth.registry:
        return jsonify({"error": "Unknown provider"}), 400

    token = oauth.create_client(provider).authorize_access_token()
    user_info = token.get("userinfo")
    if not user_info:
        return jsonify({"error": "Invalid user info"}), 400

    jwt_token = generate_jwt(user_info)  # Call function from utils.py
    return jsonify({"jwt": jwt_token, "user": user_info})
