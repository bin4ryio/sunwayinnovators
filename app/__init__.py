import os
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_rq import RQ

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()


def create_app(env):
    app = Flask(__name__, static_folder='./static/dist', template_folder='./static')
    app.config.from_object(config[env])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    config[env].init_app(app)

    # Set up extensions
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
    mail.init_app(app)
    db.init_app(app)
    RQ(app)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    from .auth.controllers import AuthLogin, AuthRegister
    api.add_resource(AuthLogin, '/auth/login')
    api.add_resource(AuthRegister, '/auth/register')

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app

    # Create app blueprints
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    # from .account import account as account_blueprint
    # app.register_blueprint(account_blueprint)
    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')
