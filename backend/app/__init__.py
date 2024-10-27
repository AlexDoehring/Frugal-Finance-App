import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import expenses_bp
from .auth import auth_bp
from flask_login import LoginManager
from .models import db, User
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

    # Check if the database file exists before loading schema
    db_path = os.path.join(app.root_path, 'app.db')
    if not os.path.exists(db_path):
        with app.app_context():
            init_db(db, app)

    return app

def init_db(db, app):
    """Initialize the database by loading schema.sql."""
    with app.app_context():
        schema_path = os.path.join(app.root_path, 'migrations/schema.sql')
        with open(schema_path) as f:
            db.session.execute(f.read())
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
