from model.User import User
from datetime import datetime, timedelta
import hashlib, base64, json, jwt
from config import app_active, app_config

config = app_config[app_active]

class UserController:

    def __init__(self):
        self.user_model = User()

    def verify_auth_token(self, access_token):
        status = 401

        try:
            jwt.decode(access_token, config.SECRET, algorithms='HS256')
            message = 'Token válido'
            status = 200
        except jwt.ExpiredSignatureError:
            message = 'Token expirado, realize login novamente'
        except:
            message = 'Token inválido'

        return {
            'message': message,
            'status': status
        }

    def generate_auth_token(self, data, exp=30, time_exp=False):
        if time_exp == True:
            date_time = data['exp']
        else:
            date_time = datetime.utcnow() + timedelta(minutes=exp)

        dict_jwt = {
            'id': data['id'],
            'username': data['username'],
            'exp': date_time
        }

        access_token = jwt.encode(dict_jwt, config.SECRET, algorithm='HS256')

        return access_token

    def login(self, email, password):
        self.user_model.email = email
        user = self.user_model.get_user_by_email()

        if user is not None:
            res = self.user_model.verify_password(password, user.password)

            if res:
                return user
            else:
                return {}

        return {}

    def recovery(self, email):
        return ''

    def get_user_by_id(self, user_id):
        result = {}
        try:
            self.user_model.id = user_id
            user = self.user_model.get_user_by_id()
            res = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_created': user.date_created
            }
            status = 200
        except Exception as e:
            print(e)
            result = {}
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }