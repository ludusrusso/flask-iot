from flask import Blueprint

api = Blueprint('api_v1', __name__)

def get_catalog():
    return {'device': [], 'user': []}

@api.route('/')
def base():
    return ''
