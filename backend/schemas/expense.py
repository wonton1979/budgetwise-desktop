from pydantic import BaseModel,Field
from decimal import Decimal
from backend.models.category import Category
from datetime import date


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "Amount of the expense"
    )
    category: Category
    description: str
    expense_date: date

class ExpenseUpdate(BaseModel):
    amount: Decimal | None = Field(default=None,gt=0,description="Amount of the expense")
    category: Category | None = None
    description: str | None = None
    expense_date: date | None = None