from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_rq import RQ


# Set up extensions
cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
redis = RQ()
