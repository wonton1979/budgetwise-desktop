from fastapi import APIRouter,HTTPException
from backend.schemas.expense import ExpenseCreate
from backend.services.expense_service import add_expense, get_all_expenses,get_expense_by_id,delete_expense_by_id


router = APIRouter()


@router.post("/expenses")
def create_expense(expense: ExpenseCreate):
    saved_expense = add_expense(expense)
    return {"message": "Expense added", "data": saved_expense}


@router.get("/expenses")
def get_expenses():
    return {"data": get_all_expenses()}

@router.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    expense = get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"data": expense}

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    expense = delete_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}