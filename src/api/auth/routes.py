from flask import Blueprint
from src.api.auth.services import google_auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/api/auth/google", methods=["POST"])
def auth_google():
    return google_auth()