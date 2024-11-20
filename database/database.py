from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

engine = create_engine("postgresql://scott:tiger@localhost/mydatabase")

db = SQLAlchemy(model_class=Base)

def init_app(app: Flask):
    db.init_app(app)

def create_all(app: Flask):
    with app.app_context():
        db.create_all()

