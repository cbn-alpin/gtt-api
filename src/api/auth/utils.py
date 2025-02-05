import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET")

def generate_jwt(user_info):
    return jwt.encode(
        {
            "sub": user_info["sub"],
            "email": user_info["email"],
            "name": user_info.get("name", ""),
            "exp": datetime.utcnow() + timedelta(hours=1),
        },
        JWT_SECRET,
        algorithm="HS256",
    )
