from flask import Blueprint

from voluptuous import Schema, Required
from .decorators import json, expected_json
from .models import User

api = Blueprint('api_v1', __name__)

def get_catalog():
    return {'device': [], 'user': []}

login_schema = Schema({
    Required('username'): str,
    Required('password'): str
})

@api.route('/login', methods=['POST'])
@expected_json(login_schema, 'login')
@json
def login(login):
    user = User.query.filter_by(username=login['username']).first()
    if user is None or not user.check_password(login['password']):
        return {'msg': 'username or password not correct'}, 401
    return {'token': user.generate_auth_token().decode('UTF-8')}

@api.route('/')
def base():
    return ''
