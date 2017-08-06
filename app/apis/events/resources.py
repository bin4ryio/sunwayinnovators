from flask import jsonify
from flask_restplus import Namespace, Resource, fields, reqparse

from . import controllers
from .. import helpers
from ...extensions import jwt


api = Namespace('events', description='Events')


resource_fields = api.model('Resource', {
})
