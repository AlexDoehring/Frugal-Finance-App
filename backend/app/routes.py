from flask import Blueprint, request, jsonify
from .models import Expense, User, Budget, Income
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from datetime import datetime, time, timedelta
from .db import db
from io import StringIO, BytesIO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

expenses_bp = Blueprint('expenses', __name__)
budget_bp = Blueprint('budget', __name__)
income_bp = Blueprint('income', __name__)
export_bp = Blueprint('export', __name__)
settings_bp = Blueprint('settings', __name__)


@export_bp.route('/export_csv', methods=['GET'])
@login_required
def export_csv():
    # Query the data
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    
    # Create a CSV file in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['Type', 'ID', 'Amount', 'Category', 'Description', 'Date/Source/Frequency'])
    
    # Write expenses
    for expense in expenses:
        writer.writerow(['Expense', expense.id, expense.amount, expense.category, expense.description, expense.date])
    
    # Write incomes
    for income in incomes:
        writer.writerow(['Income', income.id, income.amount, income.source_name, income.description, income.frequency])
    
    # Write budgets
    for budget in budgets:
        writer.writerow(['Budget', budget.id, budget.amount, budget.category, budget.description, ''])
    
    # Move the cursor to the beginning of the StringIO object
    output.seek(0)
    
    # Return the CSV file as a response
    return output.getvalue(), 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=export.csv'}

@export_bp.route('/export_pdf', methods=['GET'])
@login_required
def export_pdf():
    # Query the data
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    
    # Create a CSV file in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['Type', 'ID', 'Amount', 'Category', 'Description', 'Date/Source/Frequency'])
    
    # Write expenses
    for expense in expenses:
        writer.writerow(['Expense', expense.id, expense.amount, expense.category, expense.description, expense.date])
    
    # Write incomes
    for income in incomes:
        writer.writerow(['Income', income.id, income.amount, income.source_name, income.description, income.frequency])
    
    # Write budgets
    for budget in budgets:
        writer.writerow(['Budget', budget.id, budget.amount, budget.category, budget.description, ''])
    
    # Move the cursor to the beginning of the StringIO object
    output.seek(0)
    
    # Read the CSV data
    csv_data = list(csv.reader(output))
    
    # Create a PDF in memory
    pdf_output = BytesIO()
    pdf = SimpleDocTemplate(pdf_output, pagesize=letter)
    
    # Create a table with the CSV data
    table = Table(csv_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data rows background
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Build the PDF
    pdf.build([table])
    
    # Get the PDF data and set the response headers
    pdf_output.seek(0)
    
    return pdf_output.getvalue(), 200, {'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename=export.pdf'}
    

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

def check_budget(budget, total_expenses, category):
    category = str(category).strip("()\',")
    if budget and total_expenses > budget.amount:
        return f'Warning: this expense exceeds your budget for this category: {category}'
    if budget and budget.amount - total_expenses <= budget.threshold:
        return f'Warning: you are approaching your budget for this category: {category}'
    return None

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
        
        # Calculate total expenses for the category
        total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id, category=category).scalar() or 0
        print(f'total_expenses before amount added: {total_expenses}')
        total_expenses += amount
        print(f'total_expenses after amount added: {total_expenses}')
        
        # Get the budget for the category
        budget = Budget.query.filter_by(user_id=current_user.id, category=category).first()
        
        
        # Creates the new expense
        new_expense = Expense(user_id=current_user.id, amount=amount, category=category, date=date, description=description)
        
        db.session.add(new_expense)  # Add the expense to the db
        db.session.commit()
        
        warning = check_budget(budget, total_expenses, category=category)
        
        if warning:
            return jsonify({'message': warning}), 201
        return jsonify({'message': 'Expense logged successfully'}), 201  # Message signaling a successful log

        # # Check if the total expenses exceed the budget threshold
        # if budget and total_expenses > budget.amount:
        #     # Message signaling a successful log with a warning
        #     return jsonify({'message': 'Warning: this expense exceeds your budget for this category'}), 201  
        # # Check if total expenses are approaching the budget threshold
        # if budget and budget.amount - total_expenses <= budget.threshold:
        #     # Message signaling a successful log with a warning
        #     return jsonify({'message': 'Warning: you are approaching your budget for this category'}), 201
        # return jsonify({'message': 'Expense logged successfully'}), 201  # Message signaling a successful log 
    
    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400  # Invalid data type
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Other exceptions

@expenses_bp.route('/expenses/csv', methods=['POST'])
@login_required
def import_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']  # Get the CSV file from the request
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file or not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format. Please upload a CSV file'}), 400

    try:
        stream = StringIO(file.stream.read().decode('UTF-8'))
        csv_input = csv.reader(stream)
        headers = [header.lower() for header in next(csv_input)]
        
        for row in csv_input:
            data = dict(zip(headers, row))
            for key in data:
                data[key] = data[key].strip()
                if key == 'amount':
                    amount = float(data[key])
                if key == 'date':
                    if isinstance(data[key], str):
                        data[key] = datetime.strptime(data[key], '%m/%d/%Y').date()
                    elif isinstance(data[key], datetime):
                        data[key] = data[key].date()
                    date = data[key]
                if key == 'description':
                    description = data[key]
                if key == 'category':
                    category = data[key]
            is_valid, error_message = validate_input(data)
            if not is_valid:
                return jsonify({'error': error_message}), 400

            new_expense = Expense(user_id=current_user.id, amount=amount, category=category, date=date, description=description)
            db.session.add(new_expense)
            
        db.session.commit() # Commit the changes to the database

        total_expenses = 0
        total_warnings = ''
        for category in db.session.query(Expense.category).filter_by(user_id=current_user.id).distinct():
            total_expenses += db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id, category=category[0]).scalar() or 0
            budget = Budget.query.filter_by(user_id=current_user.id, category=category[0]).first()
            warning = check_budget(budget, total_expenses, category)
            if warning:
                total_warnings += warning + '; '
        if total_warnings:
            total_warnings = total_warnings.rstrip('; ')
            total_warnings = total_warnings.replace('Warning: ', '')
            return jsonify({'message': total_warnings}), 201
        
        return jsonify({'message': 'Expenses imported successfully'}), 201

    except Exception as e:
        db.session.rollback() # Rollback the changes if an error occurs
        return jsonify({'error': str(e)}), 500

@expenses_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    """
    Preconditions: User must be registered and logged in
    Acceptable Input: Optional query parameters: category, start_date, end_date, time_span, page, per_page
    Postconditions: Returns a paginated list of expenses 
    Return Values: JSON with total expenses, page details, and filtered list
    Side Effects: None
    Known Faults: None
    """
    # Optional filters retrieved from front end 
    category = request.args.get('category')  
    start_date = request.args.get('start_date')  
    end_date = request.args.get('end_date')  
    time_span = request.args.get('time_span')  # New time_span parameter
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
    if time_span:
        now = datetime.now()
        if time_span == '1month':
            start_date = now - timedelta(days=30)
        elif time_span == '3months':
            start_date = now - timedelta(days=90)
        elif time_span == '6months':
            start_date = now - timedelta(days=180)
        elif time_span == '1year':
            start_date = now - timedelta(days=365)
        else:
            return jsonify({"error": "Invalid time span"}), 400
        query = query.filter(Expense.date >= start_date.date())

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
@expenses_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
@login_required
def edit_expense(expense_id):
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Valid JSON payload with optional amount, category, date, description fields.
    Postconditions: Updates the specified expense entry in the database.
    """
    data = request.get_json()
    
    # Find the expense by ID and ensure it belongs to the current user
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if not expense:
        return jsonify({'error': 'Expense not found or access unauthorized'}), 404

    # Validate input fields if they are provided in the data
    if 'amount' in data:
        try:
            expense.amount = float(data['amount'])
            if expense.amount <= 0:
                return jsonify({'error': 'Amount must be a positive number'}), 400
        except ValueError:
            return jsonify({'error': 'Amount must be a valid number'}), 400

    if 'category' in data:
        expense.category = data['category']
    
    if 'date' in data:
        try:
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Date must be in YYYY-MM-DD format'}), 400
    
    if 'description' in data:
        expense.description = data['description']

    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'}), 200

@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Expense ID as URL parameter.
    Postconditions: Deletes the specified expense from the database.
    """
    # Find the expense by ID and ensure it belongs to the current user
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    if not expense:
        return jsonify({'error': 'Expense not found or access unauthorized'}), 404

    # Delete the expense from the database
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'}), 200

#BUDGET
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
        threshold = float(data['threshold'])
        category = data['category']
        description = data.get('description', None)

        new_budget = Budget(user_id=current_user.id, amount=amount, threshold=threshold, category=category, description=description)

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
            'threshold' : budget.threshold,
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

@budget_bp.route('/budget/<int:budget_id>', methods=['PUT'])
@login_required
def edit_budget(budget_id):
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Valid JSON payload with optional amount, category, description fields.
    Postconditions: Updates the specified budget entry in the database.
    """
    data = request.get_json()
    
    # Find the budget by ID and ensure it belongs to the current user
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
    if not budget:
        return jsonify({'error': 'Budget not found or access unauthorized'}), 404

    # Validate input fields if they are provided in the data
    if 'amount' in data:
        try:
            budget.amount = float(data['amount'])
            if budget.amount <= 0:
                return jsonify({'error': 'Amount must be a positive number'}), 400
        except ValueError:
            return jsonify({'error': 'Amount must be a valid number'}), 400
        
    if 'threshold' in data:
        try:
            budget.threshold = float(data['threshold'])
            if budget.threshold <= 0:
                return jsonify({'error': 'Threshold must be a positive number'}), 400
        except ValueError:
            return jsonify({'error': 'Threshold must be a valid number'}), 400

    if 'category' in data:
        budget.category = data['category']
    
    if 'description' in data:
        budget.description = data['description']

    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Budget updated successfully'}), 200

@budget_bp.route('/budget/<int:budget_id>', methods=['DELETE'])
@login_required
def delete_budget(budget_id):
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Budget ID as URL parameter.
    Postconditions: Deletes the specified budget from the database.
    """
    # Find the budget by ID and ensure it belongs to the current user
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
    if not budget:
        return jsonify({'error': 'Budget not found or access unauthorized'}), 404

    # Delete the budget from the database
    db.session.delete(budget)
    db.session.commit()
    return jsonify({'message': 'Budget deleted successfully'}), 200


def validate_income_input(data): #Function to validate the input of data to the income table
    """
    Validates JSON input data for creating an income entry.
    Preconditions: JSON data must include 'amount', 'source_name', and 'frequency'.
    Postconditions: Returns True if data is valid, otherwise False and an error message.
    """
    fields = ['amount', 'source_name', 'frequency'] 
    for field in fields:
        if field not in data or not data[field]: # Check to make sure each field is filled 
            return False, f'{field} is required'

    try:
        amount = float(data['amount']) #Try to cast input to a float 
        if amount <= 0:
            return False, 'Amount must be a positive number'
    except ValueError:
        return False, 'Amount must be a valid number'

    return True, None #If valid, return True with no error message 

@income_bp.route('/income', methods=['POST'])
@login_required    
def add_income():
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Valid JSON payload with amount, source_name, frequency, optional description.
    Postconditions: Adds a new income entry to the database.
    """
    data = request.get_json()
    is_valid, error_message = validate_income_input(data)  #Sends retrieved data to validate input function
    if not is_valid:
        return jsonify({'error': error_message}), 400 #retrun respective error message if input was not valid 

    try: #create an instance of the income class with the input data and adds to to the database 
        amount = float(data['amount'])
        source_name = data['source_name']
        frequency = data['frequency']
        description = data.get('description', None)

        new_income = Income(user_id=current_user.id, amount=amount, source_name=source_name, frequency=frequency, description=description)

        db.session.add(new_income)
        db.session.commit()

        return jsonify({'message': 'Income source logged successfully'}), 201

    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@income_bp.route('/income', methods=['GET'])
@login_required
def get_income(): #route
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Optional query parameters: source_name, frequency, page, per_page.
    Postconditions: Returns a paginated list of income sources for the current user.
    """
    source_name = request.args.get('source_name')
    frequency = request.args.get('frequency')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Income.query.filter_by(user_id=current_user.id) #allows a user to query by source name and or frequency 
    if source_name:
        query = query.filter(Income.source_name == source_name)
    if frequency:
        query = query.filter(Income.frequency == frequency)

    incomes = query.paginate(page=page, per_page=per_page, error_out=False)
    
    #returns the results as a list of dictionaries
    result = [ 
        {
            'id': income.id,
            'source_name': income.source_name,
            'amount': income.amount,
            'frequency': income.frequency,
            'description': income.description
        } for income in incomes.items
    ]
    # Success response with paginated results
    return jsonify({
        'total': incomes.total,
        'pages': incomes.pages,
        'current_page': incomes.page,
        'incomes': result
    }), 200


@income_bp.route('/income/<int:income_id>', methods=['PUT'])
@login_required
def edit_income(income_id):
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Valid JSON payload with optional amount, source_name, frequency, description fields.
    Postconditions: Updates the specified income entry in the database.
    """
    data = request.get_json()
    
    # Find the income by ID and ensure it belongs to the current user
    income = Income.query.filter_by(id=income_id, user_id=current_user.id).first()
    if not income:
        return jsonify({'error': 'Income not found or access unauthorized'}), 404

    # Validate input fields if they are provided in the data
    if 'amount' in data:
        try:
            income.amount = float(data['amount'])
            if income.amount <= 0:
                return jsonify({'error': 'Amount must be a positive number'}), 400
        except ValueError:
            return jsonify({'error': 'Amount must be a valid number'}), 400

    if 'source_name' in data:
        income.source_name = data['source_name']
    
    if 'frequency' in data:
        income.frequency = data['frequency']
    
    if 'description' in data:
        income.description = data['description']

    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Income updated successfully'}), 200

@income_bp.route('/income/<int:income_id>', methods=['DELETE'])
@login_required
def delete_income(income_id):
    """
    Preconditions: User must be registered and logged in.
    Acceptable Input: Income ID as URL parameter.
    Postconditions: Deletes the specified income from the database.
    """
    # Find the income by ID and ensure it belongs to the current user
    income = Income.query.filter_by(id=income_id, user_id=current_user.id).first()
    if not income:
        return jsonify({'error': 'Income not found or access unauthorized'}), 404

    # Delete the income from the database
    db.session.delete(income)
    db.session.commit()
    return jsonify({'message': 'Income deleted successfully'}), 200

@settings_bp.route('/notifications', methods=['POST'])
@login_required
def set_notifications():
    data = request.get_json()
    notifications = data.get('notifications', None)
    notification_time = data.get('notification_time', None)  # Format: "HH:MM"

    if notifications is None:
        return jsonify({"error": "Notifications preference is required"}), 400

    current_user.notifications = bool(notifications)

    if notification_time:
        try:
            current_user.notification_time = time.fromisoformat(notification_time)
        except ValueError:
            return jsonify({"error": "Invalid time format"}), 400

    db.session.commit()
    return jsonify({"message": "Notification settings updated successfully"}), 200