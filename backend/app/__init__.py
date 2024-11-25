# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from .routes import expenses_bp, budget_bp, income_bp, export_bp
from .auth import auth_bp
from flask_login import LoginManager
from .models import User, Expense, Budget
from .db import db
from sqlalchemy import text
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

print("Initializing app module")

login_manager = LoginManager()
celery = None

def send_email():
    sender_email = "frugalfinanceapp@gmail.com"
    password = "uwra usgn jmij raam"
    receiver_email = "marktmaloney18@gmail.com"

    subject = "Test Email"
    body = "Log yo damn expenses boy"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Test email sent successfully to {receiver_email}!")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")

def create_app(config_class=Config):
    global celery
    print("create_app function called")
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    print("Creating app")
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(export_bp)

    with app.app_context():
        from . import models
        db.create_all()

    # Initialize and start the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started...")

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