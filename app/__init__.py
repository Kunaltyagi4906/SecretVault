from flask_session import Session
import os
from datetime import timedelta

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.secret_key = 'myvault-genz-rockzz-4321'

    # ✅ Session Configurations
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'  # 🛠️ this is the fix
    app.permanent_session_lifetime = timedelta(minutes=60)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # 🧠 Don't forget to initialize Flask-Session
    from flask_session import Session
    Session(app)

    # 🔗 Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(vault)
    app.register_blueprint(main)

    return app
