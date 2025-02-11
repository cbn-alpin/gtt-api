

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from src import api
from src.api import user
from src.api.auth.schema import AuthInputSchema
from src.api.exception import MissingFieldError, NotFoundError
from src.api import db
import hashlib

from functools import wraps

from src.models import User
print(hashlib.md5("whatever your string is".encode('utf-8')).hexdigest())


def gtt_auth(data: AuthInputSchema) -> user :
    login = data["login"]
    password = data["password"]
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    user = (
        db.session.query(User).filter(User.email == login and User.password == hashed_password).first()
    )
    db.session.close()
    if user:
        if user.is_admin:
            role = "admin"
        else:
            role = "user"
        identity = data['login']

        access_token = create_access_token(identity=identity, additional_claims={"role": role})
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

def google_auth():
    pass


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"msg": "Admin access required."}, 403
        return fn(*args, **kwargs)
    return wrapper
