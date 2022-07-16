import os
from flask import Flask, jsonify
from controllers import api_v1
from get_db import get_db


app = Flask(__name__);

app.secret_key= os.environ.get("SECRET")
app.register_blueprint(api_v1, url_prefix="/api/v1/");
with app.app_context():
    get_db();

@app.route('/', methods=["GET"])
def index():
    return "<h1>Hello @Sloovi API developed by Kehinde Fasunle</h1>"

@app.errorhandler(404)
def not_found(error):
    print(error)
    return jsonify({
        "code": 404,
        "message": "Not found"
    })
    
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "code": 500,
        "message": "Server error"
    }), 500