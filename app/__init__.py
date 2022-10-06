from flask import Flask
from config.get_configs import get_app_config


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(get_app_config(env_name))
    register_blueprints(app)
    return app


def register_blueprints(app):
    from app.home.views import home_bp
    app.register_blueprint(home_bp)

