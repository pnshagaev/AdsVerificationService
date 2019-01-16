from flask_script import Manager
from src.app import flask_app as app, build_db
manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=True)


@manager.command
def build_test_db():
    build_db()


if __name__ == "__main__":
    manager.run()



