from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import controllers  # noqa
from . import models  # noqa
