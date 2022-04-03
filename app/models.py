from uuid import uuid4
from flask_login import UserMixin
from datetime import datetime, timedelta
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, email: str, password_hash: str):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return "<User %r>" % self.name

class ConfirmationEmail(db.Model):
    __tablename__ = "confirmation_emails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    token = db.Column(db.String(128))
    expiry_date = db.Column(db.DateTime)

    def __init__(self, email: str):
        self.email = email
        self.token = uuid4().hex
        self.expiry_date = datetime.now() + timedelta(hours=24)

    def __repr__(self):
        return "<ConfirmationEmail %r>" % self.email