from flask import Flask
from flask_cors import CORS  # Import CORS
from .routes import expenses_bp
from .auth import auth_bp
from flask_login import LoginManager
from .models import User
from .db import db
from sqlalchemy import text
from config import Config
import os

login_manager = LoginManager()

def create_app(config_class=Config): 
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app) 

    # Enable CORS for all routes
    CORS(app, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)

    with app.app_context():
        from . import models  
        db.create_all()  

    return app

def init_db(db, app):
    """Initialize the database by loading schema.sql."""
    with app.app_context():
        schema_path = os.path.join(app.root_path, 'migrations/schema.sql')
        with open(schema_path) as f:
            sql_statements = f.read().split(';')  
            for statement in sql_statements:
                if statement.strip():  
                    db.session.execute(text(statement.strip())) 
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    from .models import User  
    return User.query.get(int(user_id))
