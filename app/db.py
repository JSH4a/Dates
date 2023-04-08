from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init(app):
    ab.db_init(app)

    with app.app_context():
        db.create_all()
