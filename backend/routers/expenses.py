from decimal import Decimal
from fastapi import APIRouter,HTTPException,Depends
from datetime import date
from backend.models.category import Category
from backend.models.order import Order
from backend.models.sort_by import SortBy
from backend.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseSingleResponse, \
    ExpenseListResponse
from backend.services.expense_service import (add_expense, get_all_expenses,
                                              get_expense_by_id,delete_expense_by_id,
                                              update_expense_by_id,patch_expense_by_id)
from backend.routers.users import get_current_user


router = APIRouter()

@router.get("/expenses",response_model=ExpenseListResponse)
def get_expenses(category:Category|None = None, min_amount: Decimal | None = None,max_amount: Decimal | None = None,
                 start_date:date | None = None,end_date:date | None = None,sort_by:SortBy | None = None,
                 order:Order|None = None,page:int|None = None,limit:int|None = None,current_user = Depends(get_current_user)):
    result = get_all_expenses(category,min_amount,max_amount,start_date,end_date,sort_by,order,page,limit,current_user.id)
    if len(result["data"]) == 0:
        return {
            "data":result["data"],
            "total":result["total"],
            "page":result["page"],
            "limit":result["limit"],
            "total_pages":0,
            "message": "No expense found"
        }
    if result["limit"] :
        total_pages = result["total"] // result["limit"] if result["total"] % result["limit"] == 0 \
            else result["total"] // result["limit"] + 1
    else:
        total_pages = 1
    return  {
        "data":result["data"],
        "total":result["total"],
        "page":result["page"],
        "limit":result["limit"],
        "total_pages": total_pages,
        "message":"List of expenses found",
    }

@router.post("/expenses",response_model=ExpenseSingleResponse)
def create_expense(expense: ExpenseCreate,current_user = Depends(get_current_user)):
    saved_expense = add_expense(expense,current_user.id)
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