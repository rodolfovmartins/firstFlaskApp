# -*- coding: utf-8 -*-
from flask import Flask
from config import app_config, app_active

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        return "Flask app runing..."

    return app