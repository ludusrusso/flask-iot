from flask import Flask

def create_app():
    app = Flask(__name__)
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .api_v1 import api as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app
