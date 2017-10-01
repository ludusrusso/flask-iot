from functools import wraps, partial
from flask import request, jsonify
from voluptuous import Invalid

def _expected(schema, name, location):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kargs):
            try:
                request_locs = schema(dict(getattr(request, location)))
            except Invalid as e:
                res = jsonify({'msg': str(e)})
                res.status_code = 406
                return res
            kargs[name] = request_locs
            return f(*args, **kargs)
        return wrapper
    return decorator


expected_body = partial(_expected, location='form')
expected_args = partial(_expected, location='args')
expected_json = partial(_expected, location='json')



def json(f):
    @wraps(f)
    def wrapper(*args, **kargs):
        ret = f(*args, **kargs)
        if isinstance(ret, tuple) and len(ret) == 2 and isinstance(ret[1], int):
            res =  jsonify(ret[0])
            res.status_code = ret[1]
            return res
        else:
            return jsonify(ret)
    return wrapper
