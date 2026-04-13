from fastapi import APIRouter
from backend.schemas.expense import ExpenseCreate
from backend.services.expense_service import add_expense, get_all_expenses


router = APIRouter()


@router.post("/expenses")
def create_expense(expense: ExpenseCreate):
    saved_expense = add_expense(expense)
    return {"message": "Expense added", "data": saved_expense}


@router.get("/expenses")
def get_expenses():
    return {"data": get_all_expenses()}