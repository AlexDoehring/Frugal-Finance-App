# config.py
import os
class Config: 
    SECRET_KEY = 'SECRET_KEY' 
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''# Flask-Mail Configuration
    MAIL_SERVER = 'smtp.your-email-provider.com'  # Replace with your SMTP server, e.g., smtp.gmail.com
    MAIL_PORT = # SMTP server port
    MAIL_USE_TLS = True 
    MAIL_USE_SSL = False  
    MAIL_USERNAME = #our app's email address
    MAIL_PASSWORD = #our app's email password
    MAIL_DEFAULT_SENDER = ('Frugal', 'our email') 

    # Celery Configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Replace with your Redis server URL
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Replace with your Redis result backend'''