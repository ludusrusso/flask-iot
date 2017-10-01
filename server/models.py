from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime, timedelta
import jwt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def query_with_token(token):
        print(token)
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithm='HS256')
        id = payload.get('user')
        return User.query.get(id)

    def generate_auth_token(self, timeout=timedelta(hours=24)):
        payload = {
            'exp': datetime.utcnow() + timeout,
            'iat': datetime.utcnow(),
            'sub': 'user_id',
            'user': self.id
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
