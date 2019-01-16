import os

from flask import Flask
from flask import url_for
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore
from src.views import MyHomeView
from src.init_test_db import build_sample_db
from src.models import db, User, Role
from src.admin import UserModelView, RoleModelView


def register_extensions(app):
    db.init_app(app)
    admin = Admin(app, name='Admin panel', base_template='my_master.html', template_mode='bootstrap3', index_view=MyHomeView())
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    return security, admin, user_datastore


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app
    # Build a sample db on the fly, if one does not exist yet.


flask_app = create_app('config.TestingConfig')
security, admin, user_datastore = register_extensions(flask_app)
app_dir = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.join(app_dir, flask_app.config['DATABASE_FILE'])


def build_db():
    build_sample_db(db, flask_app, user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
