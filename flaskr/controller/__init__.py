import json
from flask import (
    Blueprint,
    abort,
    redirect,
    request,
    url_for
)
from sloovi_utils import generate_hash, generate_token, login_required
from model import (
    User,
    Template
)

# version 1.0
api_v1 = Blueprint("api_v1", __name__)



@api_v1.route('/', methods=["GET"])
def index():
    return "<h1>Hello @Sloovi API developed by Kehinde Fasunle</h1>"


@api_v1.route("/register", methods=["POST", "GET"])
def register_user():
    """Register a new user
    
    user_params = {
                    first_name : 'lead_test@subi.com',
                    last_name : '123456'
                    email : 'lead_test@subi.com',
                    password : '123456'
                } 

    Returns:
        redirect to login route
    """
    # redirect from register_user
    if request.method == "GET":
        email = request.args.get("email")
        password = request.args.get("password")
        
        user = User.fetch(email)
        
        if user == None:
            return "Please Register and login again", 401
        
        else:
            # generate token
            return generate_token(user)
        
    # parse clients data
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    # Hash the password and save the hased one instead
    password = generate_hash( request.json.get("password"))
    
    if first_name == None and last_name == None and email == None and password == None:
        abort(400)
    name = '{} {}'.format(first_name, last_name)
    try:
    
        user = User(name, email, password)
        user.create()
    except:
        return "Failed to create a new template", 400
    
    return redirect(url_for("api_v1.login_user", email=email, password=password))


@api_v1.route("/login", methods=["POST", "GET"])
def login_user():
    """Login a user given email and password
    
    {
        email : 'lead_test@subi.com',
        password : '123456'
    } 

    Returns:
        returns login token if the user is registered otherwise, redirect to register route
    """
    
    # redirect from register_user
    if request.method == "GET":
        email = request.args.get("email")
        password = request.args.get("password")
        
        user = User.fetch(email)
        
        if user == None:
            return "Please Register and login again", 401
        
        else:
            # generate token
            return generate_token(user)
        
    # parse client data
    data = json.loads(request.data)
    password = data.get("password")
    email = data.get("email")
        
    if (email == '' or None) and (password == '' or None):
        abort(400)
        
    user = User.fetch(email)
    
    if user == None:
            return "Please Register and login again", 401
        
    # generate token
    return generate_token(user)
    



@api_v1.route("/template", methods=["GET"])
def show_all_templates():
    """Get All Template

    Returns:
        list: A list of all templates
    """
    return "Hello template"


@api_v1.route("/template/<int:id>", methods=["GET"])
def show_template_by_id(id):
    """Get A Template

    Args:
        id (int): template_id

    Returns:
        object: template
    """
    return f"Hello Template with Id {id}"


@api_v1.route("/template", methods=["POST"])
def create_template():
    """Create a new template
    
        {
            'template_name': ' ',
            'subject': ' ',
            'body': ' ',
        } 

    Returns:
        - a success message
        - created a new template
    """
    return "Created a template"


@api_v1.route("/template/<int:id>", methods=["PUT"])
def update_template(id):
    """Update Single Template

    Args:
        id (int): template_id

    Returns:
        - success message
    """
    return f"Hello Template with Id {id}"


@api_v1.route("/template/<int:id>", methods=["DELETE"])
def delete_template(id):
    """Delete Single Template

    Args:
        id (int): template_id

    Returns:
        - success message
    """
    return f"Hello Template with Id {id}"
