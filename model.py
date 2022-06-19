from pymongo import MongoClient

from config import MONGO_DATABASE_URI

client = MongoClient(MONGO_DATABASE_URI)
database = client.sloovi


class User:
    """User Model Created with PyMongo
    """
    
    def __init__(self, name, email, password_hash) -> None:
        self.name = name
        self.email = email
        self.password = password_hash
    
    def create_user(self):
        """Create a new User with name, email and password
        
        If success:
            - A new User with email {self.email} was created.
            
        If Failure:
            - status code 400

        """
        
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        
        # check if user already exist
        
        user = database.user.find({"email": self.email})
        
        # TODO: Raise an ExeptionError with proper message
        if len(user) != 0:
            return f"User with email {self.email} Already exist!", 400
        
        try:
            database.user.insert_one(user_data)
        except :
            return "An Error occured while creating a new User. Please try again!", 400
        
        return f"A new User with email {self.email} was created."