import datetime

from flask_restful import Resource, abort, fields, marshal, reqparse

from ..utils.errors import ValidationError
from .models import Event


event_fields = {
    'title': fields.String,
    'content': fields.String,
    'date_start': fields.DateTime(dt_format='rfc822'),
    'date_end': fields.DateTime(dt_format='rfc822'),
    'location': fields.String,
    'uri': fields.Url('event')
}


class EventAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('content', type=str, location='json')
        self.reqparse.add_argument(
            'date_start', type=datetime.date, location='json')
        self.reqparse.add_argument(
            'date_end', type=datetime.date, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        super(EventAPI, self).__init__()

    def get(self, id):
        event = Event.query.get(id)
        # event = [event for event in events if event['id'] == id]
        if event == None:
            abort(404, message='Event does not exist.')
        return {'event': marshal(event, event_fields)}

    def put(self, id):
        events = Event.get_all()
        event = [event for event in events if event['id'] == id]
        if len(event) == 0:
            abort(404)
        event = event[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                event[k] = v
        return {'event': marshal(event, event_fields)}

    def delete(self, id):
        events = Event.get_all()
        event = [event for event in events if event['id'] == id]
        if len(event) == 0:
            abort(404)
        events.remove(event[0])
        return {'result': True}


class EventListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('content', type=str, location='json')
        self.reqparse.add_argument(
            'date_start', type=datetime.date, location='json')
        self.reqparse.add_argument(
            'date_end', type=datetime.date, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        super(EventListAPI, self).__init__()

    def get(self):
        events = Event.get_all()
        return {'events': [marshal(event, event_fields) for event in events]}

    def post(self):
        args = self.reqparse.parse_args()
        event = {
            'title': args['title'],
            'content': args['content'],
            'date_start': args['date_start'],
            'date_end': args['date_end'],
            'location': args['location'],
        }
        Event.save(event)
        return {'task': marshal(event, event_fields)}, 201
