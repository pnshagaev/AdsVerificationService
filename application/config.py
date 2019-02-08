class DefaultConfig(object):

    # flask security settings
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_REGISTER_VIEW = "/"
    SECURITY_POST_RESET_VIEW = "/"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(DefaultConfig):

    DEBUG = True
    TESTING = True
    SECRET_KEY = "powerful secretkey"

    # Create in-memory database
    DATABASE_FILE = '/tmp/test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    SQLALCHEMY_ECHO = True

    # Flask-Security config
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # set optional bootswatch theme
    # FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '**'
    MAIL_PASSWORD = '**'


class ProdConfig(DefaultConfig):
    pass
