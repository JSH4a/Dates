'''
File to initialize `bcrypt` for Flask application.

The `flask_bcrypt` library is a Flask extension that provides
an integration of the `bcrypt` password hashing library for securely handling passwords
in a Flask application.

Author: Joshua Hitchon
Date: April 9, 2023
'''

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def bcrypt_init(app):
    bcrypt.init_app(app)
