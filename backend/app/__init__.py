from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User
from .models import User 

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    # Import blueprints here to avoid circular imports
    from .auth import auth_bp
    from .routes import expenses_bp

    app.register_blueprint(expenses_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        from . import models  # Import models after creating the app context
        db.create_all()  # Create database tables

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Import User model here to avoid circular import
    return User.query.get(int(user_id))
