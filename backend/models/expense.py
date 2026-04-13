from decimal import Decimal


class Expense:
    def __init__(self, amount: Decimal, category: str, description: str, expense_date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.expense_date = expense_date