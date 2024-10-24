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




