# Sloovi Interview

This Backend Interview tests API development.

## Main file: Project structure

```sh
├── README.md
├── app.py *** the main driver of the app. "flask run" to run after installing dependencies
├── controllers.py request handlers
├── get_db.py   configure mongoDB client pool
├── model.py    handles all database operations
├── sloovi_utils.py     Utility functions
├── validators.py       input validator module
├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
├── Procfile    Heroku Deployment script
```

## API Endpoints Examples

`GET /`

- welcome user with a simple message

Returns: <h1>Hello @Sloovi API developed by Kehinde Fasunle</h1>

`POST /api/v1/register`

- Registers a new user if not exist
- Redirect to login endpoint

Returns:  login token

`POST /api/v1/login`
 
- Login a user if already registered
- if not registered, return error message with 404

 Returns: login token

