from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db

auth_bp = Blueprint('auth', __name__)  # creates a blueprint to group authentication-related routes together

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    
    # Check if username or email already exists
    existing_user = User.query.filter((User.email == data['email']) | (User.username == data['username'])).first()
    if existing_user:
        return jsonify({"error": "Email or username already exists"}), 409

    # Create a new user
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')  # Use a valid hashing method
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')  # Use get to avoid KeyError
    password = data.get('password')

    # Check if both email and password are provided
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # logout the user and end session 
    return jsonify({'message': 'Logged out successfully'}), 200  # return success message
