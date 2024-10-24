from flask import Blueprint, request, jsonify
from .models import db, Expense, User
from flask_login import login_required, current_user
from datetime import datetime 

expenses_bp = Blueprint('expenses', __name__)

def validate_input(data): #function to validate required fields
    fields=['amount','category','date']
    for field in fields:
        if field not in data or not data[field]:
            return False, f'{field} is required'
    return True, None

@expenses_bp.route('/expenses',methods=['POST'])
@login_required
def add_expense():
    data=request.get_json()

    is_valid,error_message=validate_input(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    try:
        amount=float(data['amount'])
        category=data['category']
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        description=data.get('description', None)

        new_expense=Expense(user_id=current_user.id, amount=amount, category=category, date=date, description=description)
        
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({'message': 'Expense Logged Successfully'}), 201
    
    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500




