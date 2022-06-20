"""Sloovi Utility module
"""
from datetime import timedelta
from functools import wraps
import bcrypt
from flask import g, redirect, request, session, url_for
import jwt

from config import (
    SECRET,
    TOKEN_EXPIRES
)


def generate_token(user):
    '''Generate Token and Should expire after a set period'''
    
    expires_at = timedelta(minutes=TOKEN_EXPIRES)
    
    payload = {
        "email": user.get("email"),
        "password": user.get("password"),
        "exp": expires_at
    }
    
    # token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=TOKEN_EXPIRES))
    
    token = jwt.encode(payload, SECRET, "HS256")
    return token


def  confirm_token(token):
    '''Confirms if the token is valid'''
    claims = jwt.decode(token, SECRET, algorithms=["HS256"])
    return claims


def generate_hash(password : str) -> str:
    """Generate hashed password

        Args:
            password (String) - password string
            salt (int) - salt
            
        Return:
            String: generated hashed password
    """
    return  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password, hashed_pw: str) -> bool:
    '''Check if the password is correct'''
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bytes(hashed_pw, 'utf-8'))
    return password_hash.decode('utf-8') == hashed_pw


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get("Authorization")

        if authorization is None:
            session.clear()
            return redirect(url_for("api_v1.login_user"))
        
        token = authorization.split(' ')[1]
        claims = confirm_token(token)
        session["user"] = claims
        g.user = claims
        return func(*args, **kwargs)
    return wrapped