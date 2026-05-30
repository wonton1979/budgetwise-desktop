from fastapi import APIRouter, Depends


from backend.routers.users import get_current_user
from backend.models.user import User
from backend.services.savings_service import get_all_savings_by_user_id, add_savings, update_savings, delete_savings, \
    get_savings_by_id
from backend.schemas.savings import SavingsCreate, SavingsUpdate

router = APIRouter()


@router.get("/api/savings")
def fetch_all_savings(current_user: User = Depends(get_current_user)):

    return get_all_savings_by_user_id(current_user.id)


@router.post("/api/savings")
def add_new_savings(savings_data:SavingsCreate,current_user: User = Depends(get_current_user)):

    return add_savings(savings_data,current_user.id)


@router.patch("/api/savings/{savings_id}")
def patch_existing_savings(update_savings_data:SavingsUpdate,savings_id:int,current_user: User = Depends(get_current_user)):

    return update_savings(current_user.id,savings_id,update_savings_data)

@router.delete("/api/savings/{savings_id}")
def remove_existing_savings(savings_id:int,current_user: User = Depends(get_current_user)):

    return delete_savings(current_user.id,savings_id)

@router.get("/api/savings/{savings_id}")
def fetch_savings_by_id(savings_id:int,current_user: User = Depends(get_current_user)):

    return get_savings_by_id(current_user.id,savings_id)




