from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field



class SavingsCreate(BaseModel):
    goal_amount: Decimal = Field(
        gt = 0,
        description = "goal amount",
    )
    current_amount: Decimal = Field(
        ge=0,
        default=0,
        description="current amount",
    )
    purpose_name: str = Field(
        min_length=1,
        max_length=50
    )
    target_date: date | None =None
    notes: str | None = None

class SavingsUpdate(BaseModel):
    goal_amount: Decimal | None = Field(
        default=None,
        gt=0
    )
    current_amount: Decimal | None = Field(
        default=None,
        ge=0
    )
    purpose_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    target_date: date | None = None
    notes: str | None = None