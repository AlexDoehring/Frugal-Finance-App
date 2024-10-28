from flask import Blueprint, request, jsonify
from .models import Expense, User, Budget
from flask_login import login_required, current_user
from datetime import datetime
from .db import db

expenses_bp = Blueprint('expenses', __name__)
budget_bp = Blueprint('budget', __name__)

def validate_input(data):
    """
    Validates JSON input data for creating an expense entry.
    Preconditions: JSON data must include 'amount', 'category', and 'date'.
    Postconditions: Returns True if data is valid, otherwise False and an error message.
    Side Effects: None
    """
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
   
def add_expense():  # Adds an expense takes no parameters
    """
    Preconditions: User must be registered and logged in
    Acceptable Input: Valid JSON payload with amount, category, date, optional description
    Postconditions: Adds a new expense entry to the database.
    Return Values: JSON success or error message.
    Side Effects: Adds new entry to the 'expenses' table in the database.
    Known Faults: None
    """
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
    """
    Preconditions: User must be registered and logged in
    Acceptable Input: Optional query parameters: category, start_date, end_date, page, per_page
    Postconditions: Returns a paginated list of expenses 
    Return Values: JSON with total expenses, page details, and filtered list
    Side Effects: None
    Known Faults: None
    """
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

    expenses = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [  #returns the results as a list of dictionaries
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
    }), 200 # Success response with paginated results

def validate_budget_input(data):
    """
    Validates JSON input data for creating a budget goal.
    Preconditions: JSON data must include 'amount' and 'category'.
    Postconditions: Returns True if data is valid, otherwise False and an error message.
    """
    if 'amount' not in data or not data['amount']:
        return False, 'Amount is required'
    if 'category' not in data or not data['category']:
        return False, 'Category is required'

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, 'Amount must be a positive number'
    except ValueError:
        return False, 'Amount must be a valid number'

    return True, None

@budget_bp.route('/budget', methods=['POST'])
@login_required
def add_budget_goal():
    """
    Preconditions: User must be registered and logged in
    Acceptable Input: Valid JSON payload with amount, category, optional description
    Postconditions: Adds a new budget goal entry to the database.
    """
    data = request.get_json()
    is_valid, error_message = validate_budget_input(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    try:
        amount = float(data['amount'])
        category = data['category']
        description = data.get('description', None)

        new_budget = Budget(user_id=current_user.id, amount=amount, category=category, description=description)

        db.session.add(new_budget)
        db.session.commit()

        return jsonify({'message': 'Budget goal created successfully'}), 201

    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@budget_bp.route('/budget', methods=['GET'])
@login_required
def get_budget_goals():
    """
    Preconditions: User must be registered and logged in
    Acceptable Input: Optional query parameters: category, page, per_page
    Postconditions: Returns a paginated list of budget goals for the current user.
    """
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Budget.query.filter_by(user_id=current_user.id)
    if category:
        query = query.filter(Budget.category == category)

    budgets = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            'id': budget.id,
            'amount': budget.amount,
            'category': budget.category,
            'description': budget.description
        } for budget in budgets.items
    ]

    return jsonify({
        'total': budgets.total,
        'pages': budgets.pages,
        'current_page': budgets.page,
        'budgets': result
    }), 200