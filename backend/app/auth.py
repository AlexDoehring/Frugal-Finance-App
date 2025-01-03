# Import necessary modules and functions for authentication routes
from flask import Blueprint, request, jsonify  # Blueprint for grouping routes, request for handling HTTP requests, jsonify for JSON responses
from flask_login import login_user, logout_user, login_required  # Functions for managing user login sessions
from .models import User  # Import the User model from models for database operations
from werkzeug.security import check_password_hash, generate_password_hash  # Security functions for password hashing and checking
from .db import db  # Import the database instance for database transactions

# Creates a blueprint for authentication routes, grouping all related routes under 'auth'
auth_bp = Blueprint('auth', __name__)  

# Route for user registration
# Accepts JSON data containing username, email, and password to create a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Retrieve JSON data from the request

    # Check if a user with the same email or username already exists
    existing_user = User.query.filter((User.email == data['email']) | (User.username == data['username'])).first()
    if existing_user:
        # Return error if email or username is already taken
        return jsonify({"error": "Email or username already exists"}), 409

    # Hash the password using a secure algorithm before saving to the database
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    # Create a new user instance with provided data and hashed password
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    try:
        # Add the new user to the database and commit the transaction
        db.session.add(new_user)
        db.session.commit()
        # Return success message if registration is successful
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        # Return error message with the exception details
        return jsonify({"error": str(e)}), 500

# Route for user login
# Checks if the provided username and password match a registered user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Retrieve JSON data from the request
    username = data.get('username')  # Get username from data
    password = data.get('password')  # Get password from data

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Query the database for a user with the provided username
    user = User.query.filter_by(username=username).first()  # Query by username

    # If user exists and the password matches the stored hash, log them in
    if user and check_password_hash(user.password, password):
        login_user(user)  # Log in the user
        return jsonify({'message': 'Login successful'}), 200  # Return success message
    else:
        # Return error message if credentials are invalid
        return jsonify({'error': 'Invalid credentials'}), 401

# Route for user logout
# Logs out the current user if they are logged in
@auth_bp.route('/logout', methods=['POST'])
@login_required  # Ensures the user must be logged in to access this route
def logout():
    logout_user()  # Log out the user and end the session
    # Return success message after logout
    return jsonify({'message': 'Logged out successfully'}), 200  
