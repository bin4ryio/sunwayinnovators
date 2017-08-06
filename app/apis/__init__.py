from flask_restplus import Api

from .auth.resources import api as auth
from .users.resources import api as users

api = Api(
    title='Sunway Innovators',
    version='1.0',
    description='',
    doc='/docs',
    prefix='/api')

api.add_namespace(auth, path='/auth')
api.add_namespace(users, path='/users')
