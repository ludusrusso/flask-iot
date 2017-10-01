from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

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
