from flask import Blueprint, request, jsonify
from .models import db, Expense, User
from flask_login import login_required, current_user
from datetime import datetime

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
            return False, 'Amount must be a positive number'
    except ValueError:
        return False, 'Amount must be a valid number'

    return True, None

@expenses_bp.route('/expenses', methods=['POST'])  # Route for logging expenses
@login_required
def add_expense():  # Adds an expense 
    data = request.get_json()  # Get data from front end

    is_valid, error_message = validate_input(data)  # Validate input
    if not is_valid:  # If the data is not valid
        return jsonify({'error': error_message}), 400  # Return error message with status 400 

    try:
        amount = float(data['amount'])  # Parse amount
        category = data['category']
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        description = data.get('description', None)
        # Creates the new expense
        new_expense = Expense(user_id=current_user.id, amount=amount, category=category, date=date, description=description)
        
        db.session.add(new_expense)  # Add the expense to the db
        db.session.commit()

        return jsonify({'message': 'Expense logged successfully'}), 201  # Message signaling a successful log 
    
    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400  # Invalid data type
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Other exceptions

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

    # Optional filtering by category, start_date, end_date if provided
    if category:
        query = query.filter(Expense.category == category)
    if start_date:
        query = query.filter(Expense.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.date <= datetime.strptime(end_date, '%Y-%m-%d').date())

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
