from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
jwt = JWTManager()
db = SQLAlchemy()
