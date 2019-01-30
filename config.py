class TestingConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "powerful secretkey"
    # Create in-memory database
    DATABASE_FILE = '/tmp/test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    SQLALCHEMY_ECHO = True

    # set optional bootswatch theme
    # FLASK_ADMIN_SWATCH = 'cerulean'

    # Flask-Security config
    SECURITY_URL_PREFIX = "/"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/"
    SECURITY_POST_LOGOUT_VIEW = "/"
    SECURITY_POST_REGISTER_VIEW = "/"
    SECURITY_POST_RESET_VIEW = "/"


    # Flask-Security features
    # TODO: allow registration only for superuser
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
