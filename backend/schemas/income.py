from pydantic import BaseModel,Field
from decimal import Decimal
from backend.models.income_category import IncomeCategory
from backend.models.frequency import Frequency


class IncomeCreate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "income amount",
    )
    category: IncomeCategory
    frequency: Frequency
    source_name: str
    notes: str | None = Field(default=None,max_length=255)


class IncomeUpdate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "Amount of the expense"
    )
    category: IncomeCategory
    frequency: Frequency
    source_name: str
    notes: str | None = Field(default=None,max_length=255)
