from flask_script import Manager
from src.app import flask_app as app

manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=True)


if __name__ == "__main__":
    manager.run()



