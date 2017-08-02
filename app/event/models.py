from flask import current_app
from geoalchemy2 import Geography
from slugify import slugify

from .. import db
from ..utils.errors import ValidationError


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(50), unique=True)
    content = db.Text()
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    # location = db.Column(Geography(geometry_type='POINT', srid=4326))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, *args, **kwargs):
        """initialize with title."""
        super(Event, self).__init__(*args, **kwargs)
        self.title = kwargs['title']
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''), to_lower=True, max_length=50)

    def save(self):
        # if not 'slug' in kwargs:
        #     self.slug = slugify(self.title, to_lower=True, max_length=50)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Event.query.all()

    def __repr__(self):
        return "<Event: {}>".format(self.name)
