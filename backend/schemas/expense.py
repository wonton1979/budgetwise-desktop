from pydantic import BaseModel,Field
from decimal import Decimal


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "Amount of the expense"
    )
    category: str
    description: str
    expense_date: str