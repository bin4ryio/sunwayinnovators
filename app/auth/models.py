from flask import current_app
from jose import jwt
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256

from .. import db
from ..utils.errors import ValidationError


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    # @property
    # def password(self):
    #     raise AttributeError('`password` is not a readable attribute')

    @classmethod
    def create(cls, **kwargs):
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password_conf = kwargs.get('password_conf')
        if password != password_conf:
            raise ValidationError('Password and Confirm password need to be the same value')
        password = cls.hash_password(password)
        user = User(
            email = email,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def validate(cls, email, password):
        user = User.query.filter_by(email=email).first()

        if not user:
            raise ValidationError('User does not exist')

        _hash = user.password

        if cls.verify_password(password, _hash):
            try:
                payload = {
                    'id': user.id,
                    'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                    'iat': datetime.utcnow(),
                }
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except:
                raise ValidationError('There was a problem creating JWT token')
        else:
            raise ValidationError('Password incorrect')

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()
