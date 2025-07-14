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

  
    app.secret_key = 'myvault-genz-rockzz-4321'

    return app

