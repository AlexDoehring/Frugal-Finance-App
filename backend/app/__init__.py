from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .roots import expenses_bp
from .auth import auth_bp
from flask_login import LoginManager
from .models import User 

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(expenses_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        from . import routes, models, auth, analysis
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))