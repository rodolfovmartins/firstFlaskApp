# -*- coding: utf-8 -*-
from flask import Flask
from config import app_config, app_active
from flask_sqlalchemy import SQLAlchemy

config = app_config[app_active]
db = SQLAlchemy(config.APP)

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def index():
        return "Flask app runing..."

    @app.route('/login/')
    def login():
        return 'Tela de login'

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Tela de recuperar a senha'

    @app.route('/profile/<int:id>/')
    def profile(id):
        return 'O ID do usuário é %d' % id

    return app