# app/__init__.py

from flask import Flask
from app.auth import auth
from app.vault import vault
from app.routes import main

def create_app():
    app = Flask(__name__,
                template_folder='../templates',  # 👈 Point to root/templates
                static_folder='../static')       # 👈 Point to root/static


    app.secret_key = 'myvault-genz-rockzz-4321'

    # Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(vault)
    app.register_blueprint(main)

    return app



