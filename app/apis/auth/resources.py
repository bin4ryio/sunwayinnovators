from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, reqparse

from . import controllers
from .. import helpers

api = Namespace('auth', description='Authentication')


@api.route('/login')
class LoginAPI(Resource):

    @jwt_required
    @helpers.standardize_api_response
    def get(self):
        """HTTP GET. Get one or all users.
        :email: a string valid as object id.
        :returns: One or all available users.
        """
        return {'success': 'it works!'}

    @helpers.standardize_api_response
    def post(self):
        return {'success': 'it works!'}
