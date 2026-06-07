from backend.database import SessionLocal
from backend.models.health_record import HealthRecord
from backend.models.health_type import HealthType
from backend.models.weight_record import WeightRecord
from backend.models.blood_pressure_record import BloodPressureRecord
from backend.models.blood_sugar_record import BloodSugarRecord
from backend.models.period_record import PeriodRecord
from backend.exceptions.health_exceptions import MissingRequiredFieldError
from fastapi import HTTPException


def add_health_record(health_record, user_id):

    db = SessionLocal()

    validate_health_record(health_record)

    try:

        if health_record.health_type == HealthType.WEIGHT_RECORD:
            existing_weight = (
                db.query(HealthRecord)
                .join(WeightRecord)
                .filter(HealthRecord.user_id == user_id)
                .filter(HealthRecord.health_type == HealthType.WEIGHT_RECORD)
                .filter(WeightRecord.record_date == health_record.record_date)
                .first()
            )

            if existing_weight:
                raise HTTPException(
                    status_code=409,
                    detail="Weight record already exists for this date."
                )

        db_health_record = HealthRecord(
            health_type=health_record.health_type,
            user_id=user_id,
            notes=health_record.notes,
        )

        db.add(db_health_record)
        db.commit()
        db.refresh(db_health_record)

        if health_record.health_type == HealthType.WEIGHT_RECORD:

            db_weight_record = WeightRecord(
                health_record_id=db_health_record.id,
                weight_in_kilograms=health_record.weight_in_kilograms,
                record_date=health_record.record_date,
            )
            db.add(db_weight_record)
            db.commit()
            db.refresh(db_weight_record)

        if health_record.health_type == HealthType.BLOOD_PRESSURE_RECORD:

            db_blood_pressure_record = BloodPressureRecord(
                health_record_id = db_health_record.id,
                systolic_reading = health_record.systolic_reading,
                diastolic_reading = health_record.diastolic_reading,
                heart_rate = health_record.heart_rate,
                record_date = health_record.record_date,
                record_time = health_record.record_time,
            )
            db.add(db_blood_pressure_record)
            db.commit()
            db.refresh(db_blood_pressure_record)

        if health_record.health_type == HealthType.BLOOD_SUGAR_RECORD:

            db_blood_sugar_record = BloodSugarRecord(
                health_record_id=db_health_record.id,
                value=health_record.blood_sugar_reading,
                record_type=health_record.blood_sugar_reading_type,
                record_date=health_record.record_date,
                record_time=health_record.record_time,
            )
            db.add(db_blood_sugar_record)
            db.commit()
            db.refresh(db_blood_sugar_record)

        if health_record.health_type == HealthType.PERIOD_RECORD:

            db_period_record = PeriodRecord(
                health_record_id=db_health_record.id,
                start_date=health_record.period_start_date,
                end_date=health_record.period_end_date,
            )

            db.add(db_period_record)
            db.commit()
            db.refresh(db_period_record)

        return {"message": "Record has been created"}

    finally:
        db.close()

def get_health_record(user_id):

    db = SessionLocal()

    try:
        db_weight_records = db.query(HealthRecord, WeightRecord).filter(HealthRecord.user_id == user_id).join(
            WeightRecord).filter(WeightRecord.health_record_id == HealthRecord.id).order_by(WeightRecord.record_date.asc()).all()
        db_blood_pressure_records = db.query(HealthRecord, BloodPressureRecord).filter(
            HealthRecord.user_id == user_id).join(BloodPressureRecord).filter(
            BloodPressureRecord.health_record_id == HealthRecord.id).order_by(BloodPressureRecord.record_date.asc(),
                                                                              BloodPressureRecord.record_time.asc(),
                                                                              BloodPressureRecord.id.asc()).all()
        db_blood_sugar_records = db.query(HealthRecord, BloodSugarRecord).filter(HealthRecord.user_id == user_id).join(
            BloodSugarRecord).filter(BloodSugarRecord.health_record_id == HealthRecord.id).order_by(BloodSugarRecord.record_date.asc(),
                                                                              BloodSugarRecord.record_time.asc(),
                                                                              BloodSugarRecord.id.asc()).all()
        db_period_records = db.query(HealthRecord, PeriodRecord).filter(HealthRecord.user_id == user_id).join(
            PeriodRecord).filter(PeriodRecord.health_record_id == HealthRecord.id).order_by(PeriodRecord.start_date.desc()).all()

        health_records = {
            "weight_records": [],
            "blood_sugar_records": [],
            "blood_pressure_records": [],
            "period_records": []
        }

        if db_weight_records:

            for each_weight_record in db_weight_records:
                general_info = each_weight_record[0]
                weight_info = each_weight_record[1]
                health_records["weight_records"].append(
                    {
                        "health_record_id": weight_info.health_record_id,
                        "weight_in_kilograms": weight_info.weight_in_kilograms,
                        "record_date": weight_info.record_date,
                        "notes": general_info.notes,
                    }
                )

        if db_blood_pressure_records:
            for each_blood_pressure_record in db_blood_pressure_records:
                general_info = each_blood_pressure_record[0]
                blood_pressure_info = each_blood_pressure_record[1]
                health_records["blood_pressure_records"].append(
                    {
                        "health_record_id": blood_pressure_info.health_record_id,
                        "systolic_reading": blood_pressure_info.systolic_reading,
                        "diastolic_reading": blood_pressure_info.diastolic_reading,
                        "heart_rate": blood_pressure_info.heart_rate,
                        "record_date": blood_pressure_info.record_date,
                        "record_time": blood_pressure_info.record_time,
                        "notes": general_info.notes,
                    }
                )

        if db_period_records:
            for each_period_record in db_period_records:
                general_info = each_period_record[0]
                period_info = each_period_record[1]
                health_records["period_records"].append(
                    {
                        "health_record_id": period_info.health_record_id,
                        "start_date": period_info.start_date,
                        "end_date": period_info.end_date,
                        "notes": general_info.notes,
                    }
                )

        if db_blood_sugar_records:
            for each_blood_sugar_record in db_blood_sugar_records:
                general_info = each_blood_sugar_record[0]
                blood_sugar_info = each_blood_sugar_record[1]
                health_records["blood_sugar_records"].append(
                    {
                        "health_record_id": blood_sugar_info.health_record_id,
                        "blood_sugar_reading": blood_sugar_info.value,
                        "blood_sugar_reading_type": blood_sugar_info.record_type,
                        "record_date": blood_sugar_info.record_date,
                        "record_time": blood_sugar_info.record_time,
                        "notes": general_info.notes,
                    }
                )

        return {
            "data": health_records,
            "message": "Record has been retrieved successfully"
        }
    finally:
        db.close()

def get_health_record_by_id(health_record_id,user_id):

    db = SessionLocal()

    try:
        db_health_record = db.query(HealthRecord.health_type, HealthRecord.notes).filter(
            HealthRecord.user_id == user_id).filter(HealthRecord.id == health_record_id).first()

        if not db_health_record:
            raise HTTPException(status_code=404, detail="Record not found")

        health_record_type = check_health_type(db_health_record[0])

        db_health_record_in_details = db.query(health_record_type).filter(
            health_record_type.health_record_id == health_record_id).first()
        db_health_record_in_details.notes = db_health_record[1]

        return {
            "data": db_health_record_in_details,
            "message": "Record has been retrieved successfully"
        }
    finally:
        db.close()

def update_health_record_by_id(health_record_id,new_record_details,user_id):

    db = SessionLocal()

    try:
        db_health_record = db.query(HealthRecord).filter(
            HealthRecord.user_id == user_id).filter(HealthRecord.id == health_record_id).first()

        if not db_health_record:
            raise HTTPException(status_code=404, detail="Record not found")

        validate_health_record(new_record_details)

        update_data = new_record_details.model_dump(exclude_unset=True)

        health_record_type = check_health_type(db_health_record.health_type)

        if  "notes" in update_data and db_health_record.notes != update_data["notes"]:
            db_health_record.notes = update_data["notes"]
            db.commit()
            db.refresh(db_health_record)

        health_record_in_details = db.query(health_record_type).filter(health_record_type.health_record_id==health_record_id).first()

        update_data.pop("notes", None)
        update_data.pop("health_type", None)

        if db_health_record.health_type == HealthType.BLOOD_SUGAR_RECORD:
            if "blood_sugar_reading" in update_data:
                update_data["value"] = update_data.pop("blood_sugar_reading")

            if "blood_sugar_reading_type" in update_data:
                update_data["record_type"] = update_data.pop("blood_sugar_reading_type")

        if db_health_record.health_type == HealthType.PERIOD_RECORD:
            if "period_start_date" in update_data:
                update_data["start_date"] = update_data.pop("period_start_date")

            if "period_end_date" in update_data:
                update_data["end_date"] = update_data.pop("period_end_date")

        for field,value in update_data.items():
            setattr(health_record_in_details, field, value)

        db.commit()
        db.refresh(health_record_in_details)

        return {
            "message": "Record has been updated successfully"
        }

    finally:
        db.close()

def delete_health_record(health_record_id,user_id):

    db = SessionLocal()

    try:
        db_health_record = db.query(HealthRecord).filter(HealthRecord.user_id == user_id).filter(HealthRecord.id==health_record_id).first()

        if not db_health_record:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(db_health_record)
        db.commit()

        return {
            "message": "Record has been deleted successfully"
        }

    finally:
        db.close()



def validate_health_record(health_record):

    if (health_record.weight_in_kilograms is None and health_record.systolic_reading is None
            and health_record.diastolic_reading is None and health_record.heart_rate is None
            and health_record.blood_sugar_reading is None and health_record.period_start_date is None
            and health_record.period_end_date is None and health_record.blood_sugar_reading_type is None):
        raise MissingRequiredFieldError("Please provide at least one valid health record value.")

    if health_record.health_type == HealthType.WEIGHT_RECORD and health_record.weight_in_kilograms is None:
        raise MissingRequiredFieldError("Please provide your weight value in kilograms.")

    if health_record.health_type == HealthType.BLOOD_PRESSURE_RECORD:
        if health_record.systolic_reading is None:
            raise MissingRequiredFieldError(
                "Please provide a systolic reading."
            )

        if health_record.diastolic_reading is None:
            raise MissingRequiredFieldError(
                "Please provide a diastolic reading."
            )

    if health_record.health_type == HealthType.BLOOD_SUGAR_RECORD:
        if health_record.blood_sugar_reading is None:
            raise MissingRequiredFieldError(
                "Please provide a blood sugar reading."
            )

        if health_record.blood_sugar_reading_type is None:
            raise MissingRequiredFieldError(
                "Please provide a blood sugar reading type."
            )

    if health_record.health_type == HealthType.PERIOD_RECORD and health_record.period_start_date is None:
        raise MissingRequiredFieldError("Please provide the valid period start date.")


def check_health_type(health_record_type):
    match health_record_type:
        case HealthType.WEIGHT_RECORD: return  WeightRecord
        case HealthType.BLOOD_PRESSURE_RECORD: return BloodPressureRecord
        case HealthType.PERIOD_RECORD: return PeriodRecord
        case HealthType.BLOOD_SUGAR_RECORD: return BloodSugarRecord
