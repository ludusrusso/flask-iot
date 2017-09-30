from flask import request, jsonify, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if request.headers['Content-Type'] == 'application/json':
        return jsonify({'apis': ['/api/v1/']}), 200
    else:
        return '', 404
