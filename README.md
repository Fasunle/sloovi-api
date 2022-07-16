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

`GET /api/v1/template`

- Fetch all template
- user must be logged in before making request to this endpoint

Returns: A list of all templates

`GET /api/v1/template/1`

- Fetch a template with given id

Returns: Template object

e.g 

```json

{
    "body": "I don't want to experience any form of war in my lifetime.",
    "id": "62d20931f6d1815ea4477324",
    "subject": "War causes misfortune",
    "template_name": "War zone"
}
```

`POST /api/v1/template`

- Create a template

Returns: Template with the name: has been created!

`PUT /api/v1/template/1`

- Update a template

Returns: Return update template

e.g

```json

{
    "id": "vdaey8tw78dtas",
    "template_name": "School",
    "subject": "How to excel",
    "body": "Strong determination not to fail"
}
```

`DELETE /api/v1/template/1`

- Delete Single Template

Returns: Deleted template
