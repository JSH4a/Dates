'''
Flask application factory to create and configure a Flask app.

This module defines a Flask application factory function `create_app()` that creates
and configures a Flask app. It sets up the database connection and other configurations.

Note: This code assumes that the `db.py` module is in the same package as this module.

Author: Joshua Hitchon
Date: April 9, 2023

'''

# flask imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# custom imports
from .db import db_init
from .bcrypt import bcrypt_init
from .login_manager import login_manager_init


def create_app():
    '''
    Create and configure a Flask app.

    Returns:
        app: Flask app instance
    '''

    app = Flask(__name__)

    # Register the main blueprint
    from .routes import main, auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Set up database connection and other configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SECRET_KEY"] = "supersecret"

    # Initialize database
    db_init(app)

    # Initialize bcrypt
    bcrypt_init(app)

    # Initialize login manager
    login_manager_init(app)

    return app
