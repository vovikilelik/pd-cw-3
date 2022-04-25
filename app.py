from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from config import Config
from dao.model.user import User
from service.user import UserService
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import users_ns


def create_app(config_object):
    app = Flask(__name__)

    # Setup CORS
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_object(config_object)
    register_extensions(app)
    return app


def create_data(app, db):
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password=UserService.get_hash("my_little_pony"), name="Vasili", surname='Glebovsky')
        u2 = User(username="oleg", password=UserService.get_hash("qwerty"), name="Oleg", surname='Ivanov')
        u3 = User(username="ivan", password=UserService.get_hash("P@ssw0rd"), name="Benedict", surname='Krachnenberg')

        with db.session.begin():
            db.session.add_all([u1, u2, u3])


def register_extensions(app):
    db.init_app(app)

    # Добавляет пользователей, при необходимости раскомментировать
    # create_data(app, db)

    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
