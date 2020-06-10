import os
import random, string

class Config(object):
    CSRF_ENABLED = True
    SECRET = '3EB*Zs_O/@Y.?99>o|[N/&3v3!@Q5JV'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None

    class DevelopmentConfig(Config):
        TESTING = True
        DEBUG = True
        IP_HOST = 'localhost'
        PORT_HOST = 8000
        URL_MAIN = 'http://%s:$s' % (IP_HOST, PORT_HOST)

    class TestingConfig(Config):
        TESTING = True
        DEBUG = True
        IP_HOST = 'localhost'
        PORT_HOST = 5000
        URL_MAIN = 'http://%s:$s' % (IP_HOST, PORT_HOST)

    class ProductionConfig(Config):
        TESTING = True
        DEBUG = True
        IP_HOST = 'localhost'
        PORT_HOST = 8080
        URL_MAIN = 'http://%s:$s' % (IP_HOST, PORT_HOST)

    app_config = {
        'development': DevelopmentConfig(),
        'testing': TestingConfig(),
        'production': ProductionConfig()
    }

    app_active = os.getenv('FLASK_ENV')


