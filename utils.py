


import json

from flask import g, session
from get_db import database


def set_user_to_session():
    
    claims = g.get("user")

    email = json.loads(claims)['email']

    user = database.user.find_one({"email": email})

    if user:
        user_data = {
            "user_id": str(user.get("_id")),
            "email": user.get("email")
        }
        session["user"] = user_data
        g.user = user_data
    else:
        return {"message": "invalid_token", "code": 403}
