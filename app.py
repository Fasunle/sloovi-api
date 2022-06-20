"""Sloovi API Interview

    Author: Kehinde Fasunle
    email: kfasunle@gmail.com
"""

from flask import Flask
from flask_cors import CORS
from config import SESSION_SECRET

"""Create Flask Application and configure it

Returns:
    Object: Application instance
"""

from controller import api_v1

app = Flask(__name__)

app.config["SECRET_KEY"] = SESSION_SECRET

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(api_v1, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run()