import unittest
from backend.app import create_app, db
from backend.app.models import User, Expense

class ExpenseTrackerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config_test.Config')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
            self.assertEqual(User.query.count(), 1)

    def test_add_expense(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
            expense = Expense(user_id=user.id, amount=100.0, category='Food', date='2023-01-01', description='Lunch')
            db.session.add(expense)
            db.session.commit()
            self.assertEqual(Expense.query.count(), 1)

if __name__ == '__main__':
    unittest.main()