from pydantic import BaseModel
from decimal import Decimal


class ExpenseCreate(BaseModel):
    amount: Decimal
    category: str
    description: str
    expense_date: str