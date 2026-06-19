from datetime import date, time

from pydantic import BaseModel, Field, model_validator

from backend.models.appointment_type import AppointmentType
from backend.models.online_platform import OnlinePlatform
from backend.models.appointment_status import AppointmentStatus


class CreateAppointment(BaseModel):
    appointment_date: date
    appointment_time: time
    contact: str
    appointment_type: AppointmentType
    appointment_purpose: str
    appointment_location: str | None = None
    online_platform: OnlinePlatform | None = None
    notes: str | None = Field(default=None,max_length=255)

    @model_validator(mode="after")
    def validate_appointment_location_or_platform(self):
        if self.appointment_type == AppointmentType.IN_PERSON:
            if not self.appointment_location:
                raise ValueError("Location is required for in-person appointments")

        if self.appointment_type == AppointmentType.ONLINE:
            if not self.online_platform:
                raise ValueError("Online platform is required for online appointments")

        return self

class UpdateAppointment(BaseModel):
    appointment_date: date | None = None
    appointment_time: time | None = None
    contact: str | None = None
    appointment_type: AppointmentType | None = None
    appointment_purpose: str | None = None
    appointment_location: str | None = None
    online_platform: OnlinePlatform | None = None
    status:AppointmentStatus | None = None
    notes: str | None = Field(default=None,max_length=255)

