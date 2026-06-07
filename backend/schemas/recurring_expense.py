from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from backend.models.frequency import Frequency
from backend.models.payment_method import PaymentMethod
from backend.models.recurring_expense_category import RecurringExpenseCategory
from backend.models.recurring_expense_subcategory import RecurringSubcategory


class RecurringExpenseCreate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "Amount of the expense"
    )
    category: RecurringExpenseCategory
    subcategory: RecurringSubcategory
    provider_name: str
    frequency: Frequency
    payment_method: PaymentMethod
    start_date: date
    end_date: date | None = None
    is_public_to_family: bool
    notes: str | None = Field(default=None,max_length=255)

class RecurringExpenseUpdate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "Amount of the expense"
    )
    category: RecurringExpenseCategory
    subcategory: RecurringSubcategory
    provider_name: str
    frequency: Frequency
    payment_method: PaymentMethod
    start_date: date
    end_date: date | None = None
    is_public_to_family: bool
    notes: str | None = Field(default=None,max_length=255)
