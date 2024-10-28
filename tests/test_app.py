import unittest
import json
from datetime import datetime
from backend.app import create_app
from backend.app.db import db
from backend.app.models import User, Expense
from backend.config import BASE_DIR

class ExpenseTrackerTestCase(unittest.TestCase):
    def setUp(self):
        print("SETTING UP")
        self.app = create_app('backend.config')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        print("TEARING DOWN")
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user(self):
        with self.app.app_context():
            print("TESTING USER ADDING")
            user = User(username='AlexDoehring', email='alex.doehring2@gmail.com', password='kyleishot')
            db.session.add(user)
            db.session.commit()
            self.assertEqual(User.query.count(), 1)
            print("User added successfully")

    def test_add_expense(self):
        with self.app.app_context():
            print("TESTING EXPENSE ADDING")
            user = User(username='AlexDoehring', email='alex.doehring2@gmail.com', password='kyleishot')
            db.session.add(user)
            db.session.commit()
            expense_date = datetime.strptime('2023-01-01', '%Y-%m-%d').date() #convert date string to date object
            expense = Expense(user_id=user.id, amount=100.0, category='Food', date=expense_date, description='Lunch')
            db.session.add(expense)
            db.session.commit()
            self.assertEqual(Expense.query.count(), 1)
            print("Expense added successfully")
    
    def test_load_expenses_from_json(self):
        with self.app.app_context():
            print("TESTING LOADING EXPENSES FROM JSON")
            user = User(username='AlexDoehring', email='alex.doehring2@gmail.com', password='kyleishot')
            db.session.add(user)
            db.session.commit()

            # Load expenses from JSON file
            json_path = f'{BASE_DIR}\\app\\expenses_test_data.json'
            with open(json_path) as f:
                expenses_data = json.load(f)

            # Add expenses to the database
            for expense_data in expenses_data:
                expense_date = datetime.strptime(expense_data['date'], '%Y-%m-%d').date()  # Convert date string to date object
                expense = Expense(
                    user_id=user.id,
                    amount=expense_data['amount'],
                    category=expense_data['category'],
                    date=expense_date,
                    description=expense_data.get('description')
                )
                db.session.add(expense)
            db.session.commit()
            
            print("Expenses loaded successfully")

            # Verify the number of expenses added
            self.assertEqual(Expense.query.count(), len(expenses_data))
            
            

if __name__ == '__main__':
    unittest.main()