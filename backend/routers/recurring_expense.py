from fastapi import APIRouter,HTTPException,Depends

from backend.routers.users import get_current_user
from backend.schemas.recurring_expense import RecurringExpenseCreate, RecurringExpenseUpdate
from backend.services.recurring_expense_service import add_recurring_expense, get_recurring_expenses_by_user_id, \
    update_recurring_expense,delete_recurring_expense

router = APIRouter()

@router.post("/api/recurring-expenses")
def create_recurring_expenses_endpoint(recurring_expense:RecurringExpenseCreate,current_user = Depends(get_current_user)):
    try:
        recurring_expense = add_recurring_expense(recurring_expense,current_user.id)

        return recurring_expense

    except ValueError as error:
        raise HTTPException(status_code=400, detail="Selected subcategory does not belong to the selected category")

@router.get("/api/recurring-expenses")
def fetch_recurring_expenses_endpoint(current_user = Depends(get_current_user)):

    recurring_expense = get_recurring_expenses_by_user_id(current_user.id)

    if not recurring_expense:
        raise HTTPException(status_code=404,detail="Cannot find Recurring Expense")

    return recurring_expense

@router.patch("/api/recurring-expenses/{expense_id}")
def patch_recurring_expense_endpoint(expense_id:int,update_date:RecurringExpenseUpdate,current_user = Depends(get_current_user)):

    updated_recurring_expense = update_recurring_expense(expense_id,update_date,current_user.id)

    return updated_recurring_expense

@router.delete("/api/recurring-expenses/{expense_id}")
def delete_recurring_expense_endpoint(expense_id:int,current_user = Depends(get_current_user)):

    delete_recurring_expense(expense_id,current_user.id)

    return {"message":"Recurring Expense Deleted Successfully"}
