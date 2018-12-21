class TestingConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    FLASK_ADMIN_SWATCH = 'cerulean'  # set optional bootswatch theme
