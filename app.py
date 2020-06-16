# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, Response, json, abort
from functools import wraps
from config import app_config, app_active
from flask_sqlalchemy import SQLAlchemy
from controller.User import UserController
from controller.Product import ProductController
from admin.Admin import start_views
from flask_bootstrap import Bootstrap

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'superhero'
    db = SQLAlchemy(config.APP)
    start_views(app, db)
    Bootstrap(app)
    db.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()

            try:
                result = user.verify_auth_token(request.headers['access_token'])

                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['message'])

            except KeyError as e:
                abort(401, 'Você precisa enviar um token de acesso')

        return verify_token

    @app.route('/')
    def index():
        return "Flask app runing..."

    @app.route('/login/')
    def login():
        return render_template('login.html')

    @app.route('/login/', methods=['POST'])
    def login_post():
        user_controller = UserController()
        email = request.form['email']
        password = request.form['password']

        user = user_controller.login(email, password)
        if user:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': None})

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Tela de recuperar a senha'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user_controller = UserController()
        result = user_controller.recovery(request.form['email'])

        if result:
            return render_template('recovery.html', data={'status': 200, 'msg': 'E-mail de recuperação enviado com sucesso'})
        else:
            return render_template('recovery.html', data={'status': 401, 'msg': 'Erro ao enviar e-mail de recuperação'})

    @app.route('/product/', methods=['POST'])
    def save_products():
        product_controller = ProductController()
        result = product_controller.save_product(request.form)

        if result:
            return 'Inserido'
        else:
            return 'Não inserido'

    @app.route('/product/', methods=['PUT'])
    def update_products():
        product = ProductController()
        result = product.update_product(request.form)

        if result:
            return 'Editado'
        else:
            return 'Não editado'

    @app.route('/product/<int:id>', methods=['DELETE'])
    def delete_product(id):
        product = ProductController()
        result = product.delete_product(id)

        if result:
            return 'Deletado'
        else:
            return 'Não deletado'

    @auth_token_required
    @app.route('/products/', methods=['GET'])
    @app.route('/products/<limit>', methods=['GET'])
    def products(limit=None):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'JWT'
        }
        product_controller = ProductController()
        response = product_controller.get_products(limit)

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json', status=response['status'], headers=header)

    @app.route('/product/<product_id>', methods=['GET'])
    @auth_token_required
    def get_product(product_id):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'JWT'
        }
        product_controller = ProductController()
        response = product_controller.get_product_by_id(product_id)
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json', status=response['status'], headers=header)

    @app.route('/user/<user_id>', methods=['GET'])
    @auth_token_required
    def get_user(user_id):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'JWT'
        }
        user_controller = UserController()
        response = user_controller.get_user_by_id(user_id)
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json', status=response['status'], headers=header)

    @app.route('/login_api', methods=['POST'])
    def login_api():
        header = {}
        user_controller = UserController()

        email = request.json['email']
        password = request.json['password']

        result = user_controller.login(email, password)
        code = 401
        response = {
            'message': 'Usuário não autorizado',
            'result': []
        }

        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'date_created': result.date_created,
                    'active': result.active
                }

                header = {
                    'access_token': user_controller.generate_auth_token(result),
                    'token_type': 'JWT'
                }

                code = 200

                response['message'] = 'Login realizado com sucesso'
                response['result'] = result

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json', status=code, headers=header)

    return app