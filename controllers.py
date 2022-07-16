


import json
from flask import Blueprint, jsonify, redirect, request, url_for
from model import create_new_template, create_user, delete_template, fetch_one_template, fetch_templates, fetch_user, update_template
from sloovi_utils import generate_hash, generate_token
from validators import validate_template_data, validate_user_data, validate_user_login


api_v1  = Blueprint("v1", __name__);


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
    raw_password = request.json.get("password")
    
    # validates user payload
    error = validate_user_data(
        first_name,
        last_name,
        email,
        raw_password
    )

    name = "{} {}".format(first_name, last_name);

    if error is not None:
        return error;

    # Hash the password and save the hased one instead
    password = generate_hash(raw_password)
    info = create_user(name, email, password);
    status_code = info[1];

    if status_code != 200:
        return info;
    
    else:
        return redirect(url_for("v1.login_user", email=email, password=password))


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
        
        user = fetch_user(email)
        
        if user == None:
            return "Please Register and login again", 404
        
        else:
            # generate token
            return generate_token(user)

        
    # parse client data
    password = request.json.get("password")
    email = request.json.get("email")
        
    error = validate_user_login(email, password)
    
    if error is not None:
        return error
        
    user = fetch_user(email)
    
    if user == None:
            return "Please Register and login again", 404
        
    # generate token
    return generate_token(user)


@api_v1.route("/template", methods=["GET"])
def show_templates_controller():
    """Get All Template

    Returns:
        list: A list of all templates
    """
    
    templates = fetch_templates()
    return jsonify(templates)


@api_v1.route("/template/<string:id>", methods=["GET"])
def show_template_controller(id):
    """Get A Template

    Args:
        id (int): template_id

    Returns:
        object: template
    """
    template = fetch_one_template(id)
    return jsonify(template)


@api_v1.route("/template", methods=["POST"])
def create_template_controller():
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
    # parse data from the client
    name = request.json.get("template_name")
    subject = request.json.get("subject")
    body = request.json.get("body")

    data = {
        "template_name": name,
        "subject": subject,
        "body": body
    }
    
    error = validate_template_data(data)
    
    if error is not None:
        return error
    
    template = create_new_template(name, subject, body)
    return template


@api_v1.route("/template/<string:id>", methods=["PUT"])
def update_template_controller(id):
    """Update Single Template

    Args:
        id (int): template_id

    Returns:
        - success message
    """
    # parse data from the client
    data = json.loads(request.data)
    
    error = validate_template_data(data)
    
    if error is not None:
        return error
    
    name = data.get("template_name")
    subject = data.get("subject")
    body = data.get("body")
    
    template = update_template(id, name, subject, body)
    return template


@api_v1.route("/template/<string:id>", methods=["DELETE"])
def delete_template_controller(id):
    """Delete Single Template

    Args:
        id (int): template_id

    Returns:
        - success message
    """
    deleted_template = delete_template(id)
    if deleted_template is None:
        return f"Template with this ID: {id} does not exist!"
    
    return delete_template
