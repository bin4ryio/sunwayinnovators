from flask import Blueprint

event = Blueprint('event', __name__)

from . import controllers  # noqa
from . import models  # noqa
