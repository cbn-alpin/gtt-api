from datetime import datetime

import jwt

from src.config import get_config

config = get_config()
JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = "HS256"


def generate_jwt(user_info):
    return jwt.encode(
        {
            "sub": user_info["sub"],
            "email": user_info["email"],
            "name": user_info.get("name", ""),
            "exp": datetime.now() + config.JWT_EXPIRES_IN,
        },
        JWT_SECRET,
        algorithm="HS256",
    )
