import os
from config import config
import flask
from .auth import jwt
from . import extensions, users


basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(env):
    app = flask.Flask(__name__)
    app.config.from_object(config[env])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    config[env].init_app(app)

    register_extensions(app)
    register_blueprints(app)
    jwt.set_jwt_handlers(extensions.jwt)

    return app


def register_extensions(app):
    extensions.db.init_app(app)
    extensions.jwt.init_app(app)


def register_blueprints(app):
    app.register_blueprint(users.blueprint)
