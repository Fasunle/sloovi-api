import os

ENV = os.environ.get("ENV")
TOKEN_EXPIRES = int(os.environ.get("TOKEN_EXPIRES") ) or 15
MONGO_DATABASE_URI = os.environ.get("MONGO_DATABASE_URI") or "mongodb://localhost:27017"
SECRET = os.environ.get("SECRET") or "My Little Secret"
SESSION_SECRET = "My Name is Kehinde"