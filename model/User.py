from flask_sqlalchemy import SQLAlchemy
from config import app_active, app_config
from model.Role import Role
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import relationship

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_updated = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    recovey_code = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=True)
    role = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=True)
    funcao = relationship(Role)

    def __repr__(self):
        return '%s - %s' % (self.id, self.name)

    def get_user_by_email(self):
        return ''

    def get_user_by_id(self):
        return ''

    def update(self, obj):
        return ''

    def hash_password(self, password):
        try:
            return pbkdf2_sha256.hash(password)
        except Exception as e:
            print('Erro ao criptografar senha: %s' % e)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, password_no_hash, password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_database)
        except ValueError:
            return False
