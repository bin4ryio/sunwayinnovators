from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_rq import RQ
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# Set up extensions
cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
redis = RQ()
