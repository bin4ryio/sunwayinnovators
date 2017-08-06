from flask import jsonify
from flask_restplus import Api
from jwt.exceptions import InvalidTokenError
# from flask_jwt_extended.exceptions import JWTExtendedException

from .auth.resources import api as auth
from .events.resources import api as events
from .users.resources import api as users


class MyApi(Api):
    def handle_error(self, e):
        if isinstance(e, InvalidTokenError):
            return jsonify(
                collections.OrderedDict([
                    ('status_code', e.status_code),
                    ('error', e.error),
                    ('description', e.description),
                ])
            ), e.status_code, e.headers
        return super(MyApi, self).handle_error(e)


api = MyApi(
    title='Sunway Innovators',
    version='1.0',
    description='',
    doc='/docs',
    prefix='/api')


api.add_namespace(auth, path='/auth')
api.add_namespace(events, path='/events')
api.add_namespace(users, path='/users')
