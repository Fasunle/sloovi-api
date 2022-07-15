from flask import Flask, jsonify


app = Flask(__name__);

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