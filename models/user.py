from flask_sqlalchemy import SQLAlchemy
from src.db import db


class UserModel(db.Model):
    """
    User model.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
