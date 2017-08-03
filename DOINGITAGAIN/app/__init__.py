import os
from config import config
from flask import Flask, Blueprint
from flask_restplus import Api

from .extensions import cors, db, jwt, mail, redis

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(env):
    app = Flask(
        __name__, static_folder='./static/dist', template_folder='./static')
    app.config.from_object(config[env])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    config[env].init_app(app)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})
    jwt.init_app(app)
    mail.init_app(app)
    redis.init_app(app)

    blueprint = Blueprint('api', __name__, url_prefix="/api")

    api = Api(
        version='1.0',
        title='Sunway Innovators',
        description='Sunway Innovators API',
    )

    app.register_blueprint(api)

    from auth.controllers import api as auth
    from event.controllers import api as event
    api.add_namespace(auth)
    api.add_namespace(event)

    return app
