import os

from flask import Blueprint, Flask, jsonify

from .apis import api
from .extensions import cors, db, jwt, mail, migrate, redis


def create_app():

    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS') if os.getenv('APP_SETTINGS') else 'app.config.DevelopmentConfig'
    app.config.from_object(app_settings)

    # set up extensions
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    redis.init_app(app)

    api.init_app(app)

    return app
