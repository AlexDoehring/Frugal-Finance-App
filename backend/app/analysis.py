class ExpenseAnalysis:
    def __init__(self, expenses):
        """
        Initialize with a list of expenses.
        Each expense is a dictionary with keys: 'amount', 'category', and 'date'.
        """
        self.expenses = expenses

    def total_expenses(self):
        """
        Calculate the total amount of expenses.
        """
        return sum(expense['amount'] for expense in self.expenses)

    def expenses_by_category(self):
        """
        Calculate total expenses for each category.
        """
        category_totals = {}
        for expense in self.expenses:
            category = expense['category']
            amount = expense['amount']
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        return category_totals

    def monthly_expenses(self):
        """
        Calculate total expenses for each month.
        """
        monthly_totals = {}
        for expense in self.expenses:
            month = expense['date'][:7]  # Assuming date is in 'YYYY-MM-DD' format
            amount = expense['amount']
            if month in monthly_totals:
                monthly_totals[month] += amount
            else:
                monthly_totals[month] = amount
        return monthly_totals

    def average_expense(self):
        """
        Calculate the average expense amount.
        """
        total = self.total_expenses()
        count = len(self.expenses)
        return total / count if count > 0 else 0