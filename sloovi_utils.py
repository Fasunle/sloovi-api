"""Sloovi Utility module
"""
from functools import wraps
import os
import bcrypt
from flask import g, redirect, request, session, url_for, abort
from jose import jws

from utils import set_user_to_session


SECRET = os.environ.get("SECRET")

def generate_token(user):
    '''Generate Token and Should expire after a set period'''
    
    payload = {
        "email": user.get("email"),
    }
    
    token = jws.sign(payload, SECRET, algorithm="HS256")
    return token


def  confirm_token(token:str):
    '''Confirms if the token is valid'''

    try:
        claims = jws.verify(token, SECRET, algorithms=["HS256"]).decode("utf-8")
        return claims
    except :
        abort(401, "Invalid token")


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
            return redirect(url_for("v1.login_user"))
        
        token = authorization.split(' ')[1]
        claims = confirm_token(token)
        session["user"] = claims
        g.user = claims
        # fetch user data and include user_id
        set_user_to_session()
        return func(*args, **kwargs)
    return wrapped
