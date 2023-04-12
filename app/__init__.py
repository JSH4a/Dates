'''
Flask application factory to create and configure a Flask app.

This module defines a Flask application factory function `create_app()` that creates
and configures a Flask app. It sets up the database connection and other configurations.

Note: This code assumes that the `db.py` module is in the same package as this module.

Author: Joshua Hitchon
Date: April 9, 2023

'''
from .login_manager import login_manager_init
from .bcrypt import bcrypt_init
from .db import db_init
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import eventlet
eventlet.monkey_patch()

# flask imports

# custom imports


socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    '''
    Create and configure a Flask app.

    Returns:
        app: Flask app instance
    '''

    app = Flask(__name__)
    # Set up database connection and other configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SECRET_KEY"] = "supersecret"

    # Initialize database

    # Initialize bcrypt
    bcrypt_init(app)

    # Initialize login manager
    login_manager_init(app)

    # init socket
    socketio.init_app(app)
    from .routes import main, auth

    # Register the main blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    db_init(app)
    return app
