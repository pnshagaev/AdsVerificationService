from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    _password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    description = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_pass):
        self._password = hash_password(new_pass)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
