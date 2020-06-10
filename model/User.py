from flask_sqlalchemy import SQLAlchemy
from config import app_active, app_config
from model.Role import Role

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_updated = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    recovey_code = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=True)
    role = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=True)