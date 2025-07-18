import os
from flask import Flask
from datetime import timedelta   # 👈 add this

from app.auth import auth
from app.vault import vault
from app.routes import main

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.secret_key = 'myvault-genz-rockzz-4321'

    # ✅ Session Configurations
    app.permanent_session_lifetime = timedelta(minutes=60)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # 🔗 Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(vault)
    app.register_blueprint(main)

    return app