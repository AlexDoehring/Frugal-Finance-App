from flask import Blueprint, request, jsonify
from .models import db, Expense, User
from flask_login import login_required, current_user
from datetime import datetime 

expenses_bp = Blueprint('expenses', __name__)

def validate_input(data): #function to validate required fields
    fields=['amount','category','date'] #3 required fileds
    for field in fields:
        if field not in data or not data[field]: #iterate through the fields making sure data is present (does not check to see if data is VALID. eg: expecting a number)
            return False, f'{field} is required' #return false with error message
    return True, None #returns true with no error mesage 

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
    #optional filters retrieved from front end 
    category = request.args.get('category')  
    start_date = request.args.get('start_date')  
    end_date = request.args.get('end_date')  

    query = Expense.query.filter_by(user_id=current_user.id) #build the base query

    if category: #filters by category if specified
        query = query.filter_by(category=category)  
    
    # filters by date if specified
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= start_date)
        except ValueError:
            return jsonify({'error': 'Invalid start date format'}), 400
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= end_date)
        except ValueError:
            return jsonify({'error': 'Invalid end date format'}), 400

    expenses = query.all() #execute the query and fetch all results from filter

    #Format the results into a list of dictionaries to be returned to front end 
    result = [
        {
            'id': expense.id,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description
        } for expense in expenses
    ]

    return jsonify(result), 200 #return result list 




