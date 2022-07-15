


from flask import Blueprint, redirect, request, url_for
from model import create_user, fetch_user
from sloovi_utils import generate_hash, generate_token
from validators import validate_user_data, validate_user_login


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

    if status_code is not 200:
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