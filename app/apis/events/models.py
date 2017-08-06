# from geoalchemy2 import Geography
from slugify import slugify

from app.extensions import db

from ..common import Base


class Event(Base):
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
        """Initialize event."""
        super(Event, self).__init__(*args, **kwargs)
        self.title = kwargs['title']
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(
                kwargs.get('title', ''), to_lower=True, max_length=50)

    def __repr__(self):
        return "<Event: {}>".format(self.name)
