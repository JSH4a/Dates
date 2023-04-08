from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .db import db_init


def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    db_init(app)

    return app
