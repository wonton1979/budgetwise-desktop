from backend.database import SessionLocal
from backend.models.appointment import Appointment
from fastapi import HTTPException

from backend.models.appointment_type import AppointmentType
from backend.models.appointment_status import AppointmentStatus
from datetime import datetime


def add_appointment(appointment_data, user_id):
    db = SessionLocal()

    try:
        db_appointment = Appointment(
            appointment_date=appointment_data.appointment_date,
            appointment_time=appointment_data.appointment_time,
            appointment_location=appointment_data.appointment_location,
            contact=appointment_data.contact,
            appointment_type=appointment_data.appointment_type,
            appointment_purpose=appointment_data.appointment_purpose,
            online_platform=appointment_data.online_platform,
            notes=appointment_data.notes,
            user_id=user_id,
        )

        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)

        return {"message": "Appointment created successfully"}

    finally:

        db.close()


def get_appointments(user_id):
    db = SessionLocal()

    try:
        db_all_appointments = db.query(Appointment).filter(Appointment.user_id == user_id).order_by(Appointment.appointment_date.asc(),
                                                                       Appointment.appointment_time.asc()).all()
        if not db_all_appointments:
            raise HTTPException(status_code=404, detail="No appointments found")


        upcoming_appointments = []
        completed_appointments = []
        cancelled_appointments = []
        expired_and_missed_appointments = []

        for appointment in db_all_appointments:
            appointment_date_and_time = datetime.combine(appointment.appointment_date,appointment.appointment_time)
            if appointment_date_and_time < datetime.now() and appointment.status == AppointmentStatus.UPCOMING:
                appointment.status = AppointmentStatus.EXPIRED

            match appointment.status:
                case AppointmentStatus.UPCOMING: append_appointment_to_list(upcoming_appointments, appointment)
                case AppointmentStatus.COMPLETED: append_appointment_to_list(completed_appointments, appointment)
                case AppointmentStatus.CANCELED:  append_appointment_to_list(cancelled_appointments, appointment)
                case AppointmentStatus.EXPIRED | AppointmentStatus.MISSED: append_appointment_to_list(expired_and_missed_appointments, appointment)

        db.commit()

        return {
            "data":
                {
                    "upcoming_appointments":upcoming_appointments,
                    "completed_appointments":completed_appointments,
                    "cancelled_appointments":cancelled_appointments,
                    "expired_and_missed_appointments":expired_and_missed_appointments,
                },
            "message": "Appointments retrieved successfully"
        }

    finally:
        db.close()


def update_appointment(appointment_data, appointment_id, user_id):
    db = SessionLocal()

    try:
        db_appointment = db.query(Appointment).filter(Appointment.user_id == user_id).filter(
            Appointment.id == appointment_id).first()
        if not db_appointment:
            raise HTTPException(status_code=404, detail="No appointment found")

        updated_appointment_data = appointment_data.model_dump(exclude_unset=True)

        for key, value in updated_appointment_data.items():
            setattr(db_appointment, key, value)

        db.commit()
        db.refresh(db_appointment)

        return {"message": "Appointment updated successfully"}

    finally:
        db.close()

def delete_appointment(appointment_id,user_id):
    db = SessionLocal()

    try:
        db_appointment = db.query(Appointment).filter(Appointment.user_id == user_id).filter(
            Appointment.id == appointment_id).first()

        if not db_appointment:
            raise HTTPException(status_code=404, detail="No appointment found")

        db.delete(db_appointment)
        db.commit()

        return {"message": "Appointment deleted successfully"}
    finally:
        db.close()


def append_appointment_to_list(appointments_list, appointment_data):
    appointments_list.append(
        {
            "appointment_id": appointment_data.id,
            "appointment_date": appointment_data.appointment_date,
            "appointment_time": appointment_data.appointment_time,
            "appointment_location": appointment_data.appointment_location.title() if appointment_data.appointment_type == AppointmentType.IN_PERSON else None,
            "contact": appointment_data.contact.title(),
            "appointment_type": appointment_data.appointment_type,
            "appointment_purpose": appointment_data.appointment_purpose.title(),
            "online_platform": appointment_data.online_platform if appointment_data.appointment_type == AppointmentType.ONLINE else None,
            "status": appointment_data.status,
            "notes": appointment_data.notes.title(),
        }
    )