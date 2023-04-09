'''
File to initialize Flask-Login for user authentication in a Flask application.

The `Flask-Login` library is a Flask extension that provides
user authentication and login functionality for Flask web applications.

Note: the login_route is used when the user is redirected by the flask-login system

Author: Joshua Hitchon
Date: April 9, 2023
'''

from flask_login import LoginManager

LOGIN_ROUTE = 'main.login'  # Define the login route for the application

login_manager = LoginManager()


def login_manager_init(app):
    """
    Initializes the login manager with the Flask app.

    Args:
    - app: Flask app object

    Returns:
    - None
    """
    login_manager.init_app(app)
    # Set the login view for the login manager to the defined login route
    login_manager.login_view = LOGIN_ROUTE
