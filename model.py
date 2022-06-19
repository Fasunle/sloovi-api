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
        
        user_id = user.get("id")
        self._user.update_one({'_id': user_id}, {"$set": user_update})
        
        return f"Updated User with email {self.email}"