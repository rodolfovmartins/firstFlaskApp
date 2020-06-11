# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template
from config import app_config, app_active
from flask_sqlalchemy import SQLAlchemy
from controller.User import UserController
from admin.Admin import start_views


config = app_config[app_active]
db = SQLAlchemy(config.APP)

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
    start_views(app, db)
    db.init_app(app)

    @app.route('/')
    def index():
        return "Flask app runing..."

    @app.route('/login/')
    def login():
        return 'Tela de login'

    @app.route('/login/', methods=['POST'])
    def login_post():
        user_controller = UserController
        email = request.form['email']
        password = request.form['password']

        user = user_controller.login(email, password)
        if user:
            return redirect('/admin')
        else:
            return render_template('login.htmlm', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': None})

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Tela de recuperar a senha'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user_controller = UserController
        result = user_controller.recovery(request.form['email'])

        if result:
            return render_template('recovery.html', data={'status': 200, 'msg': 'E-mail de recuperação enviado com sucesso'})
        else:
            return render_template('recovery.html', data={'status': 401, 'msg': 'Erro ao enviar e-mail de recuperação'})

    return app