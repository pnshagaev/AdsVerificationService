from flask import Flask
from flask_admin.contrib.sqla import ModelView
from src.models import db, User, UserRoles
from flask_admin import Admin


def register_extensions(app):
    db.init_app(app)
    admin = Admin(app, name='test', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(UserRoles, db.session))


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    return app


app = create_app('config.TestingConfig')