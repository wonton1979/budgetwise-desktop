from fastapi import APIRouter,HTTPException,Depends
from starlette import status
from backend.routers.users import get_current_user
from backend.services.analysis_service import monthly_expense_analysis, get_weekly_expenses, category_analysis

router = APIRouter()

@router.get("/api/dashboard/monthly-summary")
def get_expenses_monthly_summary(year,month,current_user = Depends(get_current_user)):

    response = monthly_expense_analysis(year,month,current_user.id)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Monthly Expense Analysis Failed")

    return response

@router.get("/api/dashboard/weekly-spending-trend")
def get_weekly_expenses_summary(year,month,current_user = Depends(get_current_user)):

    response = get_weekly_expenses(year,month,current_user.id)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Load Weekly Expenses Summary Failed")

    return response

@router.get("/api/dashboard/category-breakdown")
def get_category_breakdown(year,month,current_user = Depends(get_current_user)):

    response = category_analysis(year,month,current_user.id)

    return response
