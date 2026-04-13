from fastapi import APIRouter
from backend.schemas.expense import ExpenseCreate

router = APIRouter()

expenses = []


@router.post("/expenses")
def create_expense(expense: ExpenseCreate):
    expenses.append(expense)
    return {"message": "Expense added", "data": expense}

@router.get("/expenses")
def get_expenses():
    return expenses