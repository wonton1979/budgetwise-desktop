from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from backend.schemas.health_record import HealthRecordCreateOrUpdate
from backend.routers.users import get_current_user
from backend.services.health_service import (add_health_record,get_health_record,get_health_record_by_id,
                                             update_health_record_by_id,delete_health_record)
from backend.exceptions.health_exceptions import MissingRequiredFieldError

router = APIRouter()

@router.post("/api/health")
def create_health_record(health_record:HealthRecordCreateOrUpdate, current_user = Depends(get_current_user)):
    print(health_record)
    try:
        return add_health_record(health_record,current_user.id)
    except MissingRequiredFieldError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(error))


@router.get("/api/health")
def fetch_health_records(current_user = Depends(get_current_user)):

    return get_health_record(current_user.id)

@router.get("/api/health/{health_record_id}")
def fetch_health_record_by_id(health_record_id,current_user = Depends(get_current_user)):

    return get_health_record_by_id(health_record_id,current_user.id)

@router.patch("/api/health/{health_record_id}")
def patch_health_record(health_record_id,updated_record:HealthRecordCreateOrUpdate,current_user = Depends(get_current_user)):
    try:
        return update_health_record_by_id(health_record_id,updated_record,current_user.id)
    except MissingRequiredFieldError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(error))

@router.delete("/api/health/{health_record_id}")
def remove_health_record(health_record_id,current_user = Depends(get_current_user)):

    return delete_health_record(health_record_id,current_user.id)
