from flask import Blueprint, request

from gtt.api.auth.schema import AuthInputSchema, UserAuthSchema
from gtt.api.auth.services import google_auth, gtt_auth

resources = Blueprint("auth", __name__)


@resources.route("/auth/google", methods=["POST"])
def auth_google():
    data = request.get_json()
    return google_auth(data)


@resources.route("/auth/gtt", methods=["POST"])
def auth_gtt():
    data = request.get_json()
    auth = AuthInputSchema().load(data)

    return UserAuthSchema().dump(gtt_auth(auth))
