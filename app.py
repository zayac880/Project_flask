from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from views.auth import auth_ns
from dao.model.user import User
from implemented import user_service



def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


app = create_app(Config())
app.debug = True


with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = User(username="vasya", password=user_service.make_user_password_hash("my_little_pony"), role="user")
    u2 = User(username="oleg", password=user_service.make_user_password_hash("qwerty"), role="user")
    u3 = User(username="oleg", password=user_service.make_user_password_hash("P@ssw0rd"), role="admin")

    with db.session.begin():
        db.session.add_all([u1, u2, u3])



if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
