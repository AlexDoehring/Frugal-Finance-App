from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__) #creates a blueprint to gorup authenticantion related routes together

@auth_bp.route('/login', methods=['POST']) #handles user login
def login():
    data = request.get_json() #get data from front end
    user = User.query.filter_by(email=data['email']).first() #look up user by email

    if user and check_password_hash(user.password, data['password']): #if user and password match
        login_user(user) #login user which starts a session in flask-login
        return jsonify({'message': 'Logged in successfully'}), 200 #return success
    return jsonify({'error': 'Invalid credentials'}), 401 #return error if credentials incorrect

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user() #logout the user and end session 
    return jsonify({'message': 'Logged out successfully'}), 200 #return success message