from .db import db


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float(5), nullable=False)
    long = db.Column(db.Float(5), nullable=False)
    imgID = db.Column(db.Integer)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
