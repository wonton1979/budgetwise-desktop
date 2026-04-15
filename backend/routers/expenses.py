from fastapi import APIRouter,HTTPException
from backend.models.expense import Expense
from backend.schemas.expense import ExpenseCreate, ExpenseUpdate
from backend.services.expense_service import (add_expense, get_all_expenses,
                                              get_expense_by_id,delete_expense_by_id,
                                              update_expense_by_id,patch_expense_by_id)


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

@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseCreate):
    return_expense = update_expense_by_id(expense_id, expense)
    if not return_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense updated", "data": return_expense}

@router.patch("/expenses/{expense_id}")
def partial_update_expense(expense_id: int, expense: ExpenseUpdate):
    return_expense = patch_expense_by_id(expense_id, expense)
    if not return_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense partially updated", "data": return_expense}