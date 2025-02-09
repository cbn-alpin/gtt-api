from cgitb import reset
from flask import Blueprint, redirect, request, jsonify, current_app, session, url_for
from datetime import datetime, timedelta
import os
from src.api.auth.utils import generate_jwt
from src.config import get_config
from src.models import User
from src.api import db
from authlib.integrations.flask_client import OAuth

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()  # Lazy initialization (no app passed yet)
config = get_config()

def init_oauth():
    """This function will be called later in `main.py` after the app is created."""
    oauth.init_app(current_app, cache=None)  # Force Authlib to use Flask session

    oauth.register(
        name="authentik",
        client_id=  config.GS_CLIENT_ID,
        client_secret= config.GS_PRIVATE_KEY,
        access_token_url="https://auth.cbna.com/application/o/token/",
        authorize_url="https://auth.cbna.com/application/o/authorize/",
        client_kwargs={"scope": "openid profile email"},
    )

    oauth.register(
        name="google",
        client_id= config.GS_CLIENT_ID,
        client_secret= config.GS_PRIVATE_KEY,
        server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email',
              'prompt': 'select_account',
        },
    )

@auth_bp.route("/auth/login-authentik")
def login_authentik():
    return oauth.authentik.authorize_redirect("http://localhost:5000/auth/callback/authentik")

#login for google
@auth_bp.route("/auth/google/login")
def login_google():
    try:
        redirect_uri = url_for('authorize', _external=True)
        return oauth.google.authorize_redirect(redirect_uri, state=state)  # Pass state explicitly
        # redirect_uri = "http://localhost:5000/auth/callback/google"
    except Exception as e:
        current_app.logger.error(f'Error during login:{str(e)}')
        return "Error ocurred during login", 500

    
@auth_bp.route("/authorize/google")
def authorize_google():
    token = oauth.google.authorize_access_token()
    userinfo_endpoint = oauth.google.server_metadata[userinfo_endpoint]
    resp = oauth.google.get(userinfo_endpoint)
    user_info = resp.json()
    username = user_info['email']

    user = User.query.filter_by(username=username)
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    
    session['username']=username
    session['oauth_token'] = token

    return redirect(url_for('timetable'))

@auth_bp.route('/timetable')
def timetable():
    return redirect(url_for('home'))