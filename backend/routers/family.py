from datetime import date
from decimal import Decimal

from fastapi import Depends

from backend.models.expense_category import ExpenseCategory
from backend.models.order import Order
from backend.models.sort_by import SortBy
from backend.routers.expenses import router
from backend.routers.users import get_current_user
from backend.schemas.expense import ExpenseListResponse
from backend.services.family_service import get_all_family_expenses, get_all_family_recurring_expenses


@router.get("/api/family-expenses",response_model=ExpenseListResponse)
def get_family_expenses(category: ExpenseCategory | None = None, min_amount: Decimal | None = None, max_amount: Decimal | None = None,
                        start_date:date | None = None, end_date:date | None = None, sort_by:SortBy | None = None,
                        order:Order|None = None, page:int|None = None, limit:int|None = None, current_user = Depends(get_current_user)):

    result = get_all_family_expenses(category,min_amount,max_amount,start_date,end_date,sort_by,order,page,limit,current_user)
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

@router.get("/api/family-recurring-expenses")
def fetch_family_recurring_expenses(current_user = Depends(get_current_user)):

    response = get_all_family_recurring_expenses(current_user)

    return response