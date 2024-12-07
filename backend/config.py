import os
from dotenv import load_dotenv

load_dotenv()

class Config: 
    SECRET_KEY = os.getenv('SECRET_KEY', 'DEFAULTKEY_123')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
