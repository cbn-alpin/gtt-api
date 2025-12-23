from functools import wraps

from flask import Blueprint, abort, current_app, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required

from src.api.auth.schema import AuthInputSchema, UserAuthSchema
from src.api.auth.services import google_auth, gtt_auth
from src.api.exception import MissingFieldError
from src.api.user.schema import UserSchema

resources = Blueprint("auth", __name__)


@resources.route("/api/auth/google", methods=["POST"])
def auth_google():
    data = request.get_json()
    return google_auth(data)


@resources.route("/api/auth/gtt", methods=["POST"])
def auth_gtt():
    data = request.get_json()
    auth = AuthInputSchema().load(data)

    return UserAuthSchema().dump(gtt_auth(auth))
