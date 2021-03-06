import os
import random, string

class Config(object):
    CSRF_ENABLED = True
    SECRET = '3EB*Zs_O/@Y.?99>o|[N/&3v3!@Q5JV'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:go1do2fo3@localhost:3306/livro_flask'
    SENDGRID_API_KEY = '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'

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 8000
    URL_MAIN = 'http://%s:%s' % (IP_HOST, PORT_HOST)

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 5000
    URL_MAIN = 'http://%s:%s' % (IP_HOST, PORT_HOST)

class ProductionConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 8080
    URL_MAIN = 'http://%s:%s' % (IP_HOST, PORT_HOST)

app_config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig()
}

if os.getenv('FLASK_ENV'):
    app_active = os.getenv('FLASK_ENV')
else:
    app_active = 'development'


