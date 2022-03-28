from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, name: str, email: str, password_hash: str):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return "<User %r>" % self.name


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    is_complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("todos", lazy="dynamic"))

    def __init__(self, description: str, user_id: int):
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return "<Todo %r>" % self.description
