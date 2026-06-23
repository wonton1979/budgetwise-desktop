from fastapi import APIRouter, Depends

from backend.schemas.memorable_day import CreateMemorableDay, UpdateMemorableDay
from backend.routers.users import get_current_user
from backend.services.memorable_day_service import add_memorable_day,get_memorable_days,patch_memorable_day,delete_memorable_day

router = APIRouter()

@router.post("/api/memorable-day")
def create_memorable_day(memorable_day_data: CreateMemorableDay,current_user = Depends(get_current_user)):

    response = add_memorable_day(memorable_day_data,current_user.id)

    return response


@router.get("/api/memorable-day")
def fetch_memorable_days(current_user = Depends(get_current_user)):

    response = get_memorable_days(current_user.id)

    return response

@router.patch("/api/memorable-day/{memorable_day_id}")
def update_memorable_day(memorable_day_id:int,memorable_day_data: UpdateMemorableDay,current_user = Depends(get_current_user)):

    response = patch_memorable_day(memorable_day_data,current_user.id,memorable_day_id)

    return response

@router.delete("/api/memorable-day/{memorable_day_id}")
def remove_memorable_day(memorable_day_id:int,current_user = Depends(get_current_user)):

    response =  delete_memorable_day(memorable_day_id,current_user.id)

    return response
