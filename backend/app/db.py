"""     Initializes the SQLAlchemy object to be used in the app.
        Returns:
        SQLAlchemy: The SQLAlchemy object to be used in the app
        Author: Alex Doehring
        Date: 10/27/2024
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()