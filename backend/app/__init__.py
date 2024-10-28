from flask import Flask
from .routes import expenses_bp
from .auth import auth_bp
from flask_login import LoginManager
from .models import User
from .db import db
from sqlalchemy import text

login_manager = LoginManager()

def create_app(config_class='backend.config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    # Import blueprints here to avoid circular imports
    from .auth import auth_bp  # Move this inside the function
    from .routes import expenses_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)

    with app.app_context():
        from . import models  # Import models here
        db.create_all()  # Create database tables

    return app

def init_db(db, app):
    """Initialize the database by loading schema.sql."""
    with app.app_context():
        schema_path = os.path.join(app.root_path, 'migrations/schema.sql')
        with open(schema_path) as f:
            sql_statements = f.read().split(';')  # Split SQL statements by semicolon
            for statement in sql_statements:
                if statement.strip():  # Skip empty statements
                    db.session.execute(text(statement.strip()))  # Wrap SQL statements in text
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Import User model here to avoid circular import
    return User.query.get(int(user_id))
