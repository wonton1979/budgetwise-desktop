from fastapi import APIRouter, Depends, HTTPException

from backend.routers.users import get_current_user
from backend.services.income_service import get_incomes_by_user_id,add_income,patch_income,delete_income
from backend.schemas.income import IncomeCreate,IncomeUpdate

router = APIRouter()


@router.post("/api/incomes")
def create_incomes(income_create: IncomeCreate,current_user = Depends(get_current_user)):

    response = add_income(income_create,current_user.id)

    if not response:
        raise HTTPException(status_code=404,detail="User not found")

    return response

@router.get("/api/incomes")
def fetch_incomes_by_user_id(current_user = Depends(get_current_user)):

    response = get_incomes_by_user_id(current_user.id)

    if not response:
        raise HTTPException(status_code=404,detail="User not found")

    return response

@router.patch("/api/incomes/{income_id}")

def update_income(income_id: int,update_data:IncomeUpdate,current_user = Depends(get_current_user)):

    response = patch_income(income_id,update_data,current_user.id)

    if not response:
        raise HTTPException(status_code=404,detail="User not found")

    return response

@router.delete("/api/incomes/{income_id}")
def remove_income(income_id: int,current_user = Depends(get_current_user)):

    response = delete_income(income_id,current_user.id)

    if not response:
        raise HTTPException(status_code=404,detail="User not found")

    return response