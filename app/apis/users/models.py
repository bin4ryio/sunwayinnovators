from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

from ..common import Base


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff


class Role(Base):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role: {}>".format(self.name)


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, email, password):
        self.email = email
        self.hashed_password(password)

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def hashed_password(self, password):
        self.password_hash = generate_password_hash (password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def json(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
