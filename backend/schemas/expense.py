from pydantic import BaseModel,Field
from decimal import Decimal
from backend.models.category import Category
from datetime import date

from backend.models.payment_method import PaymentMethod
from backend.models.shopping_type import ShoppingType


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(
        gt = 0,
        description = "Amount of the expense"
    )
    category: Category
    shop_name: str
    shopping_type: ShoppingType
    payment_method: PaymentMethod
    tag: str | None
    expense_date: date
    notes: str | None
    is_public_to_family: bool

class ExpenseUpdate(BaseModel):
    amount: Decimal | None = Field(default=None,gt=0,description="Amount of the expense")
    category: Category | None = None
    description: str | None = None
    expense_date: date | None = None
    is_public_to_family: bool | None = None

class ExpenseResponse(BaseModel):
    id:int
    amount: Decimal
    category: Category
    description: str
    expense_date: date
    is_public_to_family: bool

    class Config:
        from_attributes = True

class ExpenseVisibilityUpdate(BaseModel):
    is_public_to_family: bool

class ExpenseVisibilityUpdateResponse(BaseModel):
    user_id:int
    is_public_to_family: bool

    class Config:
        from_attributes = True


class ExpenseSingleResponse(BaseModel):
    data:ExpenseCreate
    message:str

class ExpenseListResponse(BaseModel):
    data:list[ExpenseResponse]
    total:int
    page: int | None
    limit: int | None
    total_pages: int
    message:str

