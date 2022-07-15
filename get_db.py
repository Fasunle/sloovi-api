import os
from flask import g
from pymongo import MongoClient
from werkzeug.local import LocalProxy

MONGO_DATABASE_URI = os.environ.get("MONGO_DATABASE_URI");
DATABASE_NAME = os.environ.get("DATABASE_NAME")



def get_db():
    """
    Configuration method to return db instance
    """

    db = getattr(g, "_database", None)
        
    if db is None:
        
        db = g._database = MongoClient(
        MONGO_DATABASE_URI,
        # Connection Pooling
        maxPoolSize=50,
        connectTimeoutMS=2500
        # Set the write timeout limit to 2500 milliseconds.
        )["sloovi"]
        
    return db

database = LocalProxy(get_db)
