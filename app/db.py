'''
File to initialize SQLAlchemy for Flask application.

The `flask_sqlalchemy` library is a Flask extension that provides
integration with the SQLAlchemy Object Relational Mapper (ORM) for working with databases
in a Flask application.

This module initializes the `SQLAlchemy` instance for connecting to a database
and creating tables using the Flask application object.

Author: Joshua Hitchon
Date: April 9, 2023

Usage:
- db can be imported to the rest of the project as needed

'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init(app):
    '''
    Initialize SQLAlchemy instance with Flask application object.

    Args:
        app: Flask application object

    Returns:
        None
    '''
    db.init_app(app)

    # if tables do not already exist, then create them
    with app.app_context():
        db.create_all()
