from flask_restful import Resource, abort, reqparse

from ..utils.errors import ValidationError
from .models import User


class LoginAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument(
            'email', type=str, help='Enter your e-mail address', required=True)
        parser.add_argument(
            'password', type=str, help='Enter your password', required=True)

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')

        try:
            token = User.validate(email, password)
            return {'token': token}
        except ValidationError as e:
            # abort(400)
            abort(400, message='Error logging in -> {}'.format(str(e)))


class RegisterAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument(
            'first_name',
            type=str,
            help='You need to enter your first name',
            required=True)
        parser.add_argument(
            'last_name',
            type=str,
            help='You need to enter your last name',
            required=True)
        parser.add_argument(
            'email',
            type=str,
            help='You need to enter your e-mail address',
            required=True)
        parser.add_argument(
            'password',
            type=str,
            help='You need to enter your chosen password',
            required=True)
        parser.add_argument(
            'password_conf',
            type=str,
            help='You need to enter the confirm password field',
            required=True)

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')
        password_conf = args.get('password_conf')
        first_name = args.get('first_name')
        last_name = args.get('last_name')

        try:
            User.create(
                email=email,
                password=password,
                password_conf=password_conf,
                first_name=first_name,
                last_name=last_name)
            return {'message': 'Successfully created your account.'}
        except ValidationError as e:
            # abort(400)
            abort(400, message='Error creating account -> {}'.format(str(e)))
