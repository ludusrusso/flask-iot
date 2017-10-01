from functools import wraps
from flask import request, url_for, make_response, g
from .models import User

def login_required_response():
    response = make_response()
    response.status_code = 401
    response.headers['location'] = url_for('api_v1.login')
    return response


def login_required(f):
    @wraps(f)
    def func_wrap(*args, **kargs):
        auth_info = request.headers.get('authentication')
        if auth_info is None or 'baerer' not in auth_info:
            return login_required_response()
        try:
            user = User.query_with_token(auth_info.split()[1])
        except:
            user = None
        if user is None:
            return login_required_response()
        g.current_user = user
        return f(*args, **kargs)
    return func_wrap
