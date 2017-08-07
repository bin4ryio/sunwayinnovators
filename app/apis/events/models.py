# from geoalchemy2 import Geography
from slugify import slugify

from app.extensions import db

from ..common import Base


class Event(Base):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(50), unique=True)
    content = db.UnicodeText()
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    # location = db.Column(Geography(geometry_type='POINT', srid=4326))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', innerjoin=True, lazy='joined')

    def __init__(self, *args, **kwargs):
        """Initialize event."""
        super(Event, self).__init__(*args, **kwargs)
        self.title = kwargs['title']
        self.set_slug(self.title)

    def __repr__(self):
        return "<Event: {}>".format(self.name)

    def get_slug(self):
        return self.slug

    def set_slug(self, title):
        if slug:
            self.slug = slugify(title, to_lower=True, max_length=50)

    def json(self):
        return {
            'id': str(self.id),
            'title': self.email,
            'slug': self.first_name,
            'content': self.last_name,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'location': self.location,
            'user_id': str(self.user_id)
        }
