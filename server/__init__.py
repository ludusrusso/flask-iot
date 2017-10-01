from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

    from .api_v1 import api as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from .api_v1 import get_catalog as v1_catalog

    @app.route('/')
    def index():
        if request.headers['Content-Type'] == 'application/json':
            return jsonify({'v1': v1_catalog()}), 200
        else:
            return '', 404

    return app
