from flask import Blueprint, redirect, request, jsonify
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
import os
from src.api.auth.utils import generate_jwt

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

# Authentik OAuth
authentik = oauth.register(
    name="authentik",
    client_id=os.getenv("AUTHENTIK_CLIENT_ID"),
    client_secret=os.getenv("AUTHENTIK_CLIENT_SECRET"),
    access_token_url="https://auth.cbna.com/application/o/token/",
    authorize_url="https://auth.cbna.com/application/o/authorize/",
    client_kwargs={"scope": "openid profile email"},
)

# Google OAuth
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile email"},
)

@auth_bp.route("/auth/login-authentik")
def login_authentik():
    return authentik.authorize_redirect("http://localhost:5000/auth/callback/authentik")

@auth_bp.route("/auth/google/login")
def login_google():
    return google.authorize_redirect("http://localhost:5000/auth/callback/google")

@auth_bp.route("/auth/callback/<provider>")
def auth_callback(provider):
    """Handles OAuth callback for both Google & Authentik."""
    if provider == "authentik":
        token = authentik.authorize_access_token()
    elif provider == "google":
        token = google.authorize_access_token()
    else:
        return jsonify({"error": "Unknown provider"}), 400

    user_info = token.get("userinfo")
    if not user_info:
        return jsonify({"error": "Invalid user info"}), 400

    jwt_token = generate_jwt(user_info)  # Call function from utils.py

    return jsonify({"jwt": jwt_token, "user": user_info})
