# Import database object from the current module's database configuration
from .db import db

# Import UserMixin from flask_login to help manage user session authentication
from flask_login import UserMixin

# User class represents a user in the application
# Inherits from UserMixin (for session management) and db.Model (for database mapping)
class User(UserMixin, db.Model):
    # Define the primary key id column, which is an integer that auto-increments
    id = db.Column(db.Integer, primary_key=True)
    
    # Define the username column, unique per user, with a maximum length of 50 characters
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # Define the email column, unique per user, with a maximum length of 100 characters
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Define the password column, which stores hashed passwords with a maximum length of 200 characters
    password = db.Column(db.String(200), nullable=False)
    notifications = db.Column(db.Boolean, default=False)
    notification_time = db.Column(db.Time, nullable=True)

# Expense class represents an expense entry associated with a specific user
# Inherits from db.Model for database mapping
class Expense(db.Model):
    # Define the primary key id column, which is an integer that auto-increments
    id = db.Column(db.Integer, primary_key=True)
    
    # Define a foreign key column user_id that references the id field in the User class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Define the amount column, which stores the expense amount as a float and cannot be null
    amount = db.Column(db.Float, nullable=False)
    
    # Define the category column, which stores the category of the expense with a maximum length of 50 characters
    category = db.Column(db.String(50), nullable=False)
    
    # Define the date column, which stores the date of the expense as a Date object and cannot be null
    date = db.Column(db.Date, nullable=False)
    
    # Define the description column, which stores additional details about the expense with a maximum length of 200 characters
    # This field is optional and can be left blank
    description = db.Column(db.String(200), nullable=True)
    
    is_recurring = db.Column(db.Boolean, default=False)
    
    recurring_frequency = db.Column(db.String(50), nullable=True)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                        #Primary key for the Income table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)           #Foreign key to associate the income entry with a specific user
    source_name = db.Column(db.String(100), nullable=False)                             #Source name for the income, max length of 100 characters
    amount = db.Column(db.Float, nullable=False)                                        #Amount of income from this source, stored as a float and cannot be null
    frequency = db.Column(db.String(50), nullable=False)                                #Frequency of income, e.g., 'monthly', 'weekly', 'one-time', max length of 50 characters
    description = db.Column(db.String(200), nullable=True)                              #Optional description for additional details about the income source, max length of 200 characters