from flask_jwt_extended import create_access_token

from app.extensions import db
from .. import helpers
from ..users.models import User


def register(email, password):
    """Register an account
    :email: a string object
    :password: a string object
    :first_name: a string object
    :last_name: a string object
    :returns: a dict with the operation result
    """
    user = User(
        email=email,
        password=password
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return {'error': 'The email {!r} already exists.'.format(email)}

    token = {'access_token': create_access_token(identity=email)}
    return {'success': token}



def login(email, password):
    """Login the user.
    :email: a string object
    :password: a string object
    :returns: a dict with the operation result
    """
    user = User.query.filter_by(email=email).first()

    if not user:
        return {'no-data': ''}

    if user.check_password(password):
        token = {'access_token': create_access_token(identity=email)}
        return {'success': token}

    return {'error': 'Invalid password.'}


def logout(identity):
    """Logout the user.
    :returns: a dict with the operation result
    """
    if not identity:
        return {'no-data': ''}

    return {'success': 'Successfully logged out.'}
