from flask import Flask
from app.auth import auth
from app.vault import vault
from app.routes import main
from utils.filters import highlight

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = 'myvault-genz-rockzz-4321'

    # 🔐 Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(vault)
    app.register_blueprint(main)

    # ✨ Custom Jinja filter
    app.jinja_env.filters['highlight'] = highlight

    return app
