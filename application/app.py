import os

from flask import Flask
from flask import url_for
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore

from application.init_test_db import build_sample_db
from application.src.models import db, User, Role
from application.src.views import MyHomeView, ClientView, UserModelView, RoleModelView
from application.src.views import mail

app = Flask(__name__)
app.config.from_object('application.config.TestingConfig')

# init db
db.init_app(app)

# init flask admin
admin = Admin(app, base_template='my_master.html', template_mode='bootstrap3', index_view=MyHomeView(url='/'))
admin.add_view(UserModelView(User, db.session, name='Пользователи'))
admin.add_view(RoleModelView(Role, db.session, name='Роли'))
admin.add_view(ClientView(name='Поиск', endpoint='client'))

#datastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
app_dir = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])

# mail
mail.init_app(app)


def build_db():
    build_sample_db(db, app, user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
