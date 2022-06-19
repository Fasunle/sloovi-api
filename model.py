from pymongo import MongoClient
from bson.json_util import dumps
from config import MONGO_DATABASE_URI

client = MongoClient(MONGO_DATABASE_URI)
database = client.sloovi


class User:
    """User Model Created with PyMongo
    """
    _user = database.user
     
    def __init__(self, name, email, password_hash) -> None:
        self.name = name
        self.email = email
        self.password = password_hash
    
    def create(self):
        """Create a new User with name, email and password
        
        If success:
            - A new User with email {self.email} was created.
            
        If Failure:
            - status code 400

        """
        
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password           # TODO: password must be hashed!
        }
        
        
        user_cursor = database.user.find_one({"email": self.email})
        user = dumps(user_cursor)
        
        # TODO: Raise an ExeptionError with proper message
        
        # check if user already exist
        if user != 'null':
            return f"User with email {self.email} Already exist!", 400
        
        else:
            # if the user does not exist already, create it
            try:
                self._user.insert_one(user_data)
            except :
                return "An Error occured while creating a new User. Please try again!", 400
            
            return f"A new User with email {self.email} was created."
        
       
    
    def fetch(self, email):
        '''Get a single User'''
        
        user = self._user.find_one({"email": email})
        
        if user == None:
            return
        
        # format the data returned
        return self.format(user)
    
    
    def format(self, user):
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
        
    def update(self):
        '''Update a User'''
        
        user_update = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        
        user = self.fetch(self.email)
        
        if user == None:
            return f"Create a User. User with email {self.email}", 404
        
        self._user.update_one({'email': self.email}, {"$set": user_update})
        
        return f"Updated User with email {self.email}"
    
    
    def delete(self):
        '''Delete a User'''
        
        user = self.fetch(self.email)
        
        if user == None:
            return f"User with email {self.email} does not exist!", 404
        
        else:
            self._user.delete_one({'email': self.email})
            return f"User with email {self.email} has been deleted!"

class Template:
    """Template Model with PyMongo"""
    
    # database template document
    _template = database.template
    
    def __init__(self, name, subject, body) -> None:
        self.name = name
        self.subject = subject
        self.body = body
        
        
    def format(self, template):
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
    
    
    def create(self):
        '''Create a new Template'''
        
        template_filter = {"name": self.name, "subject": self.subject}
        template_data = {"name": self.name, "subject": self.subject, "body": self.body}
        
        # find if template already exist
        template = self._template.find_one(template_filter)
                
        if template != None:
            return f"Template with this name '{self.name}'  and subject exist!", 400
        
        # template does not exist, so create it
        self._template.insert_one(template_data)
        
        return "Template with the name {self.name} has been created!"

      
    def fetch_all(self):
        '''Fetch all templates'''
        
        templates_cursor = self._template.find()
        
        # https://www.digitalocean.com/community/tutorials/understanding-list-comprehensions-in-python-3
        
        formatted_templates = [
            self.format(template)
            for template in templates_cursor
        ]
        
        return formatted_templates
    
    
    def fetch_one(self, name):
        """Fetch a Template with a given template name. This does not guaranty
        that the template is unique and will always be returned.
        """
        
        template = self._template.find_one({"name": name})
        
        # if template does not exist
        if template == None:
            return "Template with this name: {name} does not exist", 404
        
        return self.format(template)

    
    def update(self):
        '''Update a Template with new data. The name must be unique.'''
        
        template_update = {
            "subject": self.subject,
            "body": self.body
        }
        
        template = self._template.find_one({"name": self.name})
        
        if template == None:
            return f"There is no such template with {self.name}", 404
        
        # update a template
        self._template.update_one({"name": self.name}, {"$set": template_update})
        
        return "Template Update successfully"
                