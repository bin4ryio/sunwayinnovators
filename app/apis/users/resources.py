from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, reqparse

from . import controllers
from .. import helpers

api = Namespace('users', description='Users')


@api.route('/')
class UsersAPI(Resource):

    @helpers.standardize_api_response
    def get(self, email=None):
        """HTTP GET. Get one or all users.
        :email: a string valid as object id.
        :returns: One or all available users.
        """
        # method_decorators = [jwt_required]
        return controllers.get_users(email)
