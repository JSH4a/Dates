from flask import Blueprint, render_template, request, Response
from werkzeug.utils import secure_filename

from .models import Img, Marker
from .db import db_init, db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('base.html')


@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


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

    return render_template('db.html', img=img.img)


@main.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
