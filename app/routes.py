from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('base.html')


@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
