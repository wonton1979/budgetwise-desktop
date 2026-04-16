from decimal import Decimal
from fastapi import APIRouter,HTTPException
from datetime import date
from backend.models.category import Category
from backend.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseSingleResponse, \
    ExpenseListResponse
from backend.services.expense_service import (add_expense, get_all_expenses,
                                              get_expense_by_id,delete_expense_by_id,
                                              update_expense_by_id,patch_expense_by_id)


router = APIRouter()

@router.get("/expenses",response_model=ExpenseListResponse)
def get_expenses(category:Category|None = None, min_amount: Decimal | None = None,
                 start_date:date | None = None,end_date:date | None = None):
    all_expenses = get_all_expenses(category,min_amount,start_date,end_date)
    if len(all_expenses) == 0:
        return {
            "data": [],
            "message": "No expense found"
        }
    return  {
        "data":all_expenses,
        "message":"List of expenses found"
    }

@router.post("/expenses",response_model=ExpenseSingleResponse)
def create_expense(expense: ExpenseCreate):
    saved_expense = add_expense(expense)
    return {
        "data":saved_expense,
        "message":"Expense created"
    }

@router.get("/expenses/{expense_id}",response_model=ExpenseResponse)
def get_expense(expense_id: int):
    expense = get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    expense = delete_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}

@router.put("/expenses/{expense_id}",response_model=ExpenseSingleResponse)
def update_expense(expense_id: int, expense: ExpenseCreate):
    return_expense = update_expense_by_id(expense_id, expense)
    if not return_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense updated", "data": return_expense}

@router.patch("/expenses/{expense_id}",response_model=ExpenseSingleResponse)
def partial_update_expense(expense_id: int, expense: ExpenseUpdate):
    return_expense = patch_expense_by_id(expense_id, expense)
    if not return_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense partially updated", "data": return_expense}