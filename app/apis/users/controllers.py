from .. import helpers
from .models import User


def get_users(email=None):
    """Get all users info. Accepts specify an email.
    :email: a string object
    :returns: a dict with the operation result
    """
    users = User.query.filter_by(
        email=email).first() if email else User.query.all()

    if not users:
        return {'no-data': ''}

    return {'success': [u.json() for u in users]}
