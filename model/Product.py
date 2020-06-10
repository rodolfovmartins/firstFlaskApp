from flask_sqlalchemy import SQLAlchemy
from config import app_active, app_config
from model.User import User

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    qtd = db.Column(db.Integer, nullable=True, default=0)
    image = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullalbe=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_updated = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.Boolean(), default=1, nullalbe=True)
    user_created = db.Column(db.Integer(), db.ForeignKey(User.id), nullalbe=False)
    category = db.Column(db.Integer(), db.ForeignKey(), nullalbe=False)