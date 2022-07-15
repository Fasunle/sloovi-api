



def validate_template_data(data):
    '''Check if all data are passed correctly'''

    if data.get("template_name") is None:
        return "Template Name is Required"
    
    if data.get("subject") is None:
        return "Template Subject is Required"
    
    if data.get("body") is None:
        return "Template Body is Required"


def validate_user_login(email, password):
    '''Validates User Login data'''

    if email is None or '':
        return "Email is required", 400
    
    if password is None or '':
        return "Password is required", 
    

def validate_user_data(first_name, last_name, email, password):
    '''Validates that the User payload is correctly passed'''
    
    if first_name == None:
        return "First Name is required", 400
    
    if last_name == None:
        return "Last Name is required", 400
    
    if email == None:
        return "Email is required", 400
    
    if password == None:
        return "Password is required", 400

