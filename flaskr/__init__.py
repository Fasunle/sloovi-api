"""Sloovi API Interview

    Author: Kehinde Fasunle
    email: kfasunle@gmail.com
"""

from flask import Flask
from flaskr.controller import api_v1



def create_app():
    """Create Flask Application and configure it

    Returns:
        Object: Application instance
    """
    
    app = Flask(__name__)
    
    app.register_blueprint(api_v1, url_prefix="/api/v1")
    
    return app