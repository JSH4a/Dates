'''
This Python file contains the routing logic for the Flask web application. 

File is split into the main routing and routing to do with authetication lower down.

Note: This files imports from db.py to write to the database

Author: Joshua Hitchon
Date: April 9, 2023
'''

# flask imports
from flask import Blueprint, render_template, request, Response, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

# custom imports
from .models import Img, Marker, User, LoginForm, RegisterForm
from .db import db
from .bcrypt import bcrypt
from .login_manager import login_manager

# Register blueprints - note they are split for future modularity
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Main website routes


@main.route('/')
def index():
    return render_template('landing.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main.html')


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/db')
def db_page():
    return render_template('db.html')


@main.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    lat = 51.380741
    long = -2.360147
    print("REQUEST:", request.form.get('input-title'))
    title = request.form.get('input-title')
    desc = request.form.get('input-desc')

    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    marker = Marker(lat=lat, long=long, imgID=img.id,
                    title=title, description=desc)
    db.session.add(marker)
    db.session.commit()

    return


# authentication routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)
