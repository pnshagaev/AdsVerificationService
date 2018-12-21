from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class UserRoles(db.Model):
    """
    current supported roles:
    id = 0, role = admin
    id = 1, role = moderator
    id = 2, role = user

    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.Integer)
    roles = db.ForeignKey(UserRoles.id)

