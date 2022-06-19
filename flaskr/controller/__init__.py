from flask import (
    Blueprint,
    abort,
    redirect,
    request,
    url_for
)

from model import (
    User,
    Template
)

# version 1.0
api_v1 = Blueprint("api_v1", __name__)



@api_v1.route('/', methods=["GET"])
def index():
    return redirect(url_for("api_v1.login_user"))


@api_v1.route("/register", methods=["POST"])
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
    # parse clients data
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    # TODO: Hash the password and save the hased one instead
    password = request.json.get("password")
    
    if first_name == None and last_name == None and email == None and password == None:
        abort(400)
        
    try:
    
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()
    except:
        return "Failed to create a new template", 400
    
    return redirect(url_for("api_v1.login_user"))


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
    return "Hello login"


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