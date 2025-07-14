import os
from flask import Flask
from app.auth import auth
from app.vault import vault
from app.routes import main

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))  # /code/app
    template_dir = os.path.join(base_dir, '..', 'templates')  # /code/templates
    static_dir = os.path.join(base_dir, '..', 'static')      # /code/static

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.secret_key = 'myvault-genz-rockzz-4321'

    # Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(vault)
    app.register_blueprint(main)

    return app
