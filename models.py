from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    groups = db.relationship('Group', backref=db.backref('user', lazy=False), lazy=False)
    urls = db.relationship('Url', backref=db.backref('user', lazy=False), lazy=False)
    redirects = db.relationship('Redirect', backref=db.backref('user', lazy=False), lazy=False)
    resets = db.relationship('PasswordReset', backref=db.backref('user', lazy=False), lazy=False, uselist=False)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    urls = db.relationship('Url', cascade='all, delete-orphan', backref=db.backref('group', lazy=False), lazy=False)
    redirects = db.relationship('Redirect', cascade='all, delete-orphan', backref=db.backref('group', lazy=False), lazy=False)


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    path = db.Column(db.String(400), nullable=False)
    short_path = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    redirects = db.relationship('Redirect', cascade='all, delete-orphan', backref=db.backref('url', lazy=False), lazy=False)


class Redirect(db.Model):
    __tablename__ = 'redirects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    source = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
