from fastapi import APIRouter, Depends

from backend.schemas.appointment import CreateAppointment,UpdateAppointment
from backend.routers.users import get_current_user
from backend.services.appointment_service import add_appointment,get_appointments,update_appointment,delete_appointment

router = APIRouter()

@router.post("/api/appointment")
def create_new_appointment(appointment_data:CreateAppointment,current_user = Depends(get_current_user)):

    response = add_appointment(appointment_data,current_user.id)

    return response

@router.get("/api/appointment")
def fetch_appointments(current_user=Depends(get_current_user)):

    response = get_appointments(current_user.id)
    return response


@router.patch("/api/appointment/{appointment_id}")
def patch_appointment(updated_appointment_data:UpdateAppointment,appointment_id:int,current_user=Depends(get_current_user)):

    response = update_appointment(updated_appointment_data,appointment_id,current_user.id)

    return response

@router.delete("/api/appointment/{appointment_id}")
def delete_appointment_by_id(appointment_id:int,current_user=Depends(get_current_user)):

    response = delete_appointment(appointment_id,current_user.id)

    return response
