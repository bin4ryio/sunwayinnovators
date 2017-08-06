from flask import jsonify
from flask_jwt_extended import jwt_optional, jwt_required, get_jwt_identity
from flask_restplus import Namespace, Resource, fields, reqparse

from app.extensions import jwt
from . import controllers
from .. import helpers


api = Namespace('auth', description='Authentication')


resource_fields = api.model('Auth', {
    'email': fields.String,
    'password': fields.String,
})


@api.route('/register')
class RegisterAPI(Resource):

    @helpers.standardize_api_response
    @api.doc(body=resource_fields)
    @api.expect(resource_fields)
    def post(self):
        """HTTP POST. Login the user.
        :email: a string valid as object id.
        :password: a string valid as object id.
        :returns: authentication token of the user.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')

        return controllers.register(email, password)


@api.route('/login')
class LoginAPI(Resource):

    @helpers.standardize_api_response
    @api.doc(body=resource_fields)
    @api.expect(resource_fields)
    def post(self):
        """HTTP POST. Login the user.
        :email: a string valid as object id.
        :password: a string valid as object id.
        :returns: authentication token of the user.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')

        return controllers.login(email, password)


@api.route('/logout')
class LogoutAPI(Resource):

    @helpers.standardize_api_response
    @jwt_optional
    def post(self):
        """HTTP POST. Logout the user.
        returns:
        """
        return controllers.logout(identity=get_jwt_identity())




# Standardize JWT error response behavior
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'error': 400,
        'description': 'Bad Request',
        'data': 'The token has expired.'
    }), 400

@jwt.invalid_token_loader
def invalid_token_loader_callback():
    return jsonify({
        'error': 400,
        'description': 'Bad Request',
        'data': 'Invalid token.'
    }), 400

@jwt.unauthorized_loader
def unauthorized_loader(msg):
    return jsonify({
        'error': 400,
        'description': 'Bad Request',
        'data': 'The token is unauthorized.'
    }), 400
