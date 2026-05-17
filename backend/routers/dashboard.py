from fastapi import APIRouter,HTTPException,Depends
from starlette import status
from backend.routers.users import get_current_user
from backend.services.analysis_service import monthly_expense_analysis

router = APIRouter()

@router.get("/api/dashboard/monthly-summary")
def get_expenses_monthly_summary(year,month,current_user = Depends(get_current_user)):

    print(current_user)
    response = monthly_expense_analysis(year,month,current_user.id)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Monthly Expense Analysis Failed")

    return response
