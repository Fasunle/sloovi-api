


from bson import ObjectId
from flask import abort

from get_db import database
from sloovi_utils import generate_hash


def format_user(user):
    """Format User data

        user = {
            "name": "Kehinde Fasunle",
            "email": "kfasunle@gmail.com",
            "password": "536qrtdyugy7eq6tqet"
        }

        Note: password hash is saved to the database
    """
    return {
        "id": str(user.get("_id")),
        "name": user.get("name"),
        "email": user.get("email"),
        "password": user.get("password")
    }


def create_user(name, email, password):
    """Create a new User with name, email and password
        
    If success:
        - A new User with email was created.
        
    If Failure:
        - status code 400

    """
    
    user_data = {
        "name": name,
        "email": email,
        "password": password
    }
    
    
    user_cursor = database.user.find_one({"email": email})

    if user_cursor is None:

        try:
            database.user.insert_one(user_data)
            return f"A new User with email {email} was created.", 200
            
        except :
            return "An Error occured while creating a new User. Please try again!", 400

    else:
        return f"User with email {email} Already exist!", 400
    
    
    
def fetch_user(email):
    '''Get a single User'''
    
    user = database.user.find_one({"email": email})
    
    if user == None:
        return
    
    # format the data returned
    return format_user(user)


def update_user(name, email, password):
    '''Update a User'''

    user_update = {
        "name": name,
        "email": email,
        "password": generate_hash(password)
    }

    user = database.user.find_one({'email': email})

    if user == None:
        return f"Create a User. User with email {email}", 404

    try:
        database.user.update_one({'email': email}, {"$set": user_update})
        return f"Updated User with email {email}", 201
    except :
        return "Error occured while Updating the User", 400

    


def delete_user(email):
    '''Delete a User'''
    
    user = fetch_user(email)
    
    if user == None:
        return f"User with email {email} does not exist!", 404
    
    else:
        database.user.delete_one({'email': email})
        return f"User with email {email} has been deleted!"

        
def format_template(template):
    """Formats the Template data given a dictionary

    Args:
        template (dict): Template dictionary
            {
                "_id": "vdaey8tw78dtas",
                "template_name": "School",
                "subject": "How to excel",
                "body": "Strong determination not to fail"
            }

    Returns:
        String: Message object
    """

    return {
        "id": str(template.get("_id")),
        "template_name": template.get("name"),
        "subject": template.get("subject"),
        "body": template.get("body")
    }
    
    
def create_new_template(name, subject, body):
    '''Create a new Template'''
    
    template_filter = {"name": name, "subject": subject}
    template_data = {"name": name, "subject": subject, "body": body}
    
    # find if template already exist
    template = database.template.find_one(template_filter)
            
    if template != None:
        return f"Template with this name '{name}'  and subject exist!", 400
    
    try:
        # template does not exist, so create it
        database.template.insert_one(template_data)
    except :
        return f"Template could not be created!"
    
    return f"Template with the name {name} has been created!"


def fetch_templates():
    '''Fetch all templates'''
    
    templates_cursor = database.template.find()
    
    # https://www.digitalocean.com/community/tutorials/understanding-list-comprehensions-in-python-3
    
    formatted_templates = [
        format_template(template)
        for template in templates_cursor
    ]
    
    return formatted_templates

    
def fetch_one_template(id):
    """Fetch a Template with a given template id. This does not guaranty
    that the template is unique and will always be returned.
    """
    # placeholder
    template = None
    
    try:
        template = database.template.find_one({"_id": ObjectId(id)})
    except :
        return f"Error occured while fetching template with id: {id}"
    
    # if template does not exist
    if template == None:
        abort(404)
    
    return format_template(template)


def update_template(id, name, subject, body):
    '''Update a Template with a given id and other parameters'''
    
    template_update = {
        'name': name,
        'subject': subject,
        'body': body
    }
    
    template = None

    try:
        template = database.template.find_one_and_update({"_id": ObjectId(id)}, {"$set": template_update})
        
        if template == None:
            return f"Template with id: {id} was not found", 404
        
        template = database.template.find_one({"_id": ObjectId(id)})
    except :
        return f"Template with id: {id} couldn't update", 400
    
    return format_template(template)
        

def delete_template(id):
    '''Delete a Template and return None if not found'''
    
    deleted = database.template.find_one_and_delete({"_id": ObjectId(id)})
    
    return deleted
