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
