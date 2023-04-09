"""
This file defines the database models for the Flask application, including User, RegisterForm, LoginForm,
Img, and Marker models.

Author: Joshua Hitchon
Date: April 9, 2023
"""

# flask imports
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

# custom imports
from .db import db


class User(db.Model, UserMixin):
    """
    User model representing a user in the application.

    Attributes:
    - id (int): Primary key for the User model.
    - username (str): Username of the user.
    - password (str): Password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    """
    RegisterForm model representing the registration form in the application.

    Attributes:
    - username (str): Username entered in the registration form.
    - password (str): Password entered in the registration form.
    - submit (SubmitField): Submit button for the registration form.
    """
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    LoginForm model representing the login form in the application.

    Attributes:
    - username (str): Username entered in the login form.
    - password (str): Password entered in the login form.
    - submit (SubmitField): Submit button for the login form.
    """
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class Img(db.Model):
    """
    Img model representing an image in the application.

    Attributes:
    - id (int): Primary key for the Img model.
    - img (str): Image data stored as text.
    - name (str): Name of the image.
    - mimetype (str): MIME type of the image.
    """
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class Marker(db.Model):
    """
    Marker model representing a marker on the map in the application.

    Attributes:
    - id (int): Primary key for the Marker model.
    - lat (float): Latitude of the marker.
    - long (float): Longitude of the marker.
    - imgID (int): ID of the associated Img model for the marker image.
    - title (str): Title of the marker.
    - description (str): Description of the marker.
    """
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float(5), nullable=False)
    long = db.Column
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
