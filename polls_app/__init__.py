import os

from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


def create_app() -> Flask:
    """ Factory function for creating the Flask application"""

    app = Flask(__name__)

    db_username = os.environ.get("db_username")
    db_password = os.environ.get("db_password")

    app.config["SECRET_KEY"] = os.environ.get("secret_key")
    
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{db_username}:{db_password}@127.0.0.1/polls"
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    from polls_app.models import db

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
    
    db.init_app(app)
    app.config["db"] = db

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .polls import polls as polls_blueprint

    app.register_blueprint(polls_blueprint)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)

    with app.app_context():
        db.create_all()

    return app
