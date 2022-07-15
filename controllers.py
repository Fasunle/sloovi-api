


from crypt import methods
from flask import Blueprint


api_v1  = Blueprint("v1", __name__);


@api_v1.route("/", methods=["GET"])
def home():
    return "Hello API home route"