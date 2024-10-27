from flask import Blueprint, request, jsonify
from .models import db, Expense, User
from flask_login import login_required, current_user, login_user
from datetime import datetime 
from .analysis import ExpenseAnalysis
from .models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
expenses_bp = Blueprint('expenses', __name__)

def validate_input(data):
    fields = ['amount', 'category', 'date']
    for field in fields:
        if field not in data or not data[field]:
            return False, f'{field} is required'
    
    # Additional type checks
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, 'amount must be a positive number'
    except ValueError:
        return False, 'amount must be a valid number'
    
    return True, None

@expenses_bp.route('/expenses',methods=['POST']) #route for logging expenses
@login_required
def add_expense(): #adds an expense 
    data=request.get_json() #get data from front end

    is_valid,error_message=validate_input(data) #send data through valid function and assigns variables is_valid and error_message to the respective output from function
    if not is_valid: #if the data is not valid
        return jsonify({'error': error_message}), 400 #return error message with status 400 
    
    try:
        amount=float(data['amount'])  #tries to parse the data from the front end
        category=data['category']
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        description=data.get('description', None)
        #creates the new expense
        new_expense=Expense(user_id=current_user.id, amount=amount, category=category, date=date, description=description)
        
        db.session.add(new_expense) #adds the expense to the db
        db.session.commit()

        return jsonify({'message': 'Expense Logged Successfully'}), 201 #message signaling a successful log 
    
    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400 #if the parsing of the data fails, it was an invalid data type and returns error status 400 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@expenses_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    # Optional filters retrieved from front end 
    category = request.args.get('category')  
    start_date = request.args.get('start_date')  
    end_date = request.args.get('end_date')  
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # Default to 10 items per page

    query = Expense.query.filter_by(user_id=current_user.id)

    # ... existing filtering code ...

    expenses = query.paginate(page, per_page, error_out=False)  # Pagination

    result = [
        {
            'id': expense.id,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description
        } for expense in expenses.items
    ]

    return jsonify({
        'total': expenses.total,
        'pages': expenses.pages,
        'current_page': expenses.page,
        'expenses': result
    }), 200





