from flask import Flask
from flask_cors import CORS  # Import CORS
from .routes import expenses_bp, budget_bp, income_bp, export_bp
from .auth import auth_bp
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .models import User, Expense, Budget
from .db import db
from sqlalchemy import text
from config import Config
import os

login_manager = LoginManager()

def create_app():
    """
    Application factory function that initializes and configures the Flask app.

    Returns:
        app (Flask): The initialized Flask app.
    """
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Ensure SECRET_KEY is set for session management and Flask-Login
    if not app.config.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY is not set. Check your configuration.")

    # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy
    login_manager.init_app(app)  # Initialize Flask-Login
    login_manager.login_view = "auth.login"  # Set the login view
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"], "supports_credentials": True}})

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(export_bp)

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

@login_manager.request_loader
def load_user_from_request(request):
    # Extract the token from cookies
    token = request.cookies.get('authToken')
    if token:
        try:
            # Decode the token and get the user_id
            data = jwt.decode(token, SECRETKEY, algorithms=['HS256'])
            user_id = data.get('user_id')
            return User.query.get(user_id)  # Replace with your database lookup
        except jwt.ExpiredSignatureError:
            print("Token expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
    return None