from flask import Flask
from app.auth import auth
from app.vault import vault
from app.routes import main  # if you have it
from utils.filters import highlight

import os
from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static')
    )

    from app.auth import auth
    from app.vault import vault
    from app.routes import main

    app.register_blueprint(auth)
    app.register_blueprint(vault)
    app.register_blueprint(main)

    app.secret_key = "your_secret_key"

    return app
