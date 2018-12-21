from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config.TestingConfig')

admin = Admin(app, name='test', template_mode='bootstrap3')
db = SQLAlchemy(app)

from src.models import User
admin.add_view(ModelView(User, db.session))
