from datetime import date, time

from sqlalchemy import Date, Time, String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.models.appointment_status import AppointmentStatus
from backend.models.appointment_type import AppointmentType
from backend.models.online_platform import OnlinePlatform


class Appointment(Base):

    __tablename__ = 'appointments'

    id: Mapped [int] = mapped_column(primary_key=True,autoincrement=True)
    appointment_date: Mapped [date] = mapped_column(Date,nullable=False)
    appointment_time: Mapped [time] = mapped_column(Time,nullable=False)
    contact: Mapped [str] = mapped_column(String,nullable=False)
    appointment_type: Mapped [AppointmentType] = mapped_column(Enum(AppointmentType),nullable=False)
    appointment_purpose: Mapped [str] = mapped_column(String,nullable=False)
    appointment_location: Mapped [str|None] = mapped_column(String,default=None,nullable=True)
    online_platform: Mapped [OnlinePlatform|None] = mapped_column(Enum(OnlinePlatform),default=None,nullable=True)
    status: Mapped [AppointmentStatus] = mapped_column(Enum(AppointmentStatus),default=AppointmentStatus.UPCOMING,nullable=False)
    notes: Mapped [str|None] = mapped_column(String(255),default=None,nullable=True)
    user_id: Mapped [int] = mapped_column(ForeignKey("users.id"),nullable=False)
    user = relationship("User", back_populates="appointments")
