from backend.database import SessionLocal
from backend.models.memorable_day import MemorableDay
from backend.models.user import User
from datetime import date

def add_memorable_day(memorable_day_data,user_id):

    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details= "Can not find the user")

        memorable_day = MemorableDay(
            memorable_date = memorable_day_data.memorable_date,
            memorable_day_type = memorable_day_data.memorable_day_type,
            event_name = memorable_day_data.event_name,
            notes= memorable_day_data.notes,
            user_id = user_id
        )

        db.add(memorable_day)
        db.commit()
        db.refresh(memorable_day)

        return {"message":"New Memorable Day added!"}

    finally:
        db.close()

def get_memorable_days(user_id):

    db = SessionLocal()

    try:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Can not find the user")

        db_memorable_days = db.query(MemorableDay).filter(MemorableDay.user_id == user_id).limit(11).offset(0).all()

        memorable_days = []

        today = date.today()

        for each_memorable_day in db_memorable_days:
            memorable_day_month = each_memorable_day.memorable_date.month
            memorable_day_day = each_memorable_day.memorable_date.day
            memorable_this_year = date(today.year,memorable_day_month,memorable_day_day)

            if today > memorable_this_year:
                next_memorable_day_date = date(today.year+1,memorable_day_month,memorable_day_day)
            else:
                next_memorable_day_date = memorable_this_year

            days_remaining = (next_memorable_day_date - today).days

            memorable_days.append({
                "id": each_memorable_day.id,
                "memorable_date": each_memorable_day.memorable_date,
                "memorable_day_type": each_memorable_day.memorable_day_type,
                "event_name": each_memorable_day.event_name,
                "notes": each_memorable_day.notes,
                "days_remaining": days_remaining
            })

        memorable_days.sort(key=lambda x: x["days_remaining"])

        return {
            "data": memorable_days,
            "message": "Memorable days retrieved successfully",
        }
    finally:
        db.close()


def patch_memorable_day(memorable_day_data,user_id, memorable_day_id):

    db = SessionLocal()

    try:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Can not find the user")

        db_existing_memorable_day = db.query(MemorableDay).filter(MemorableDay.id == memorable_day_id).first()

        updated_memorable_day_data = memorable_day_data.model_dump(exclude_unset=True)

        for index,value in updated_memorable_day_data.items():
            setattr(db_existing_memorable_day,index,value)

        db.commit()
        db.refresh(db_existing_memorable_day)

        return {"message":"Memorable Day updated successfully!"}

    finally:
        db.close()


def delete_memorable_day(memorable_day_id,user_id):

    db = SessionLocal()

    try:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Can not find the user")

        db_existing_memorable_day = db.query(MemorableDay).filter(MemorableDay.id == memorable_day_id).first()

        if not db_existing_memorable_day:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Can not find the memorable day")

        db.delete(db_existing_memorable_day)
        db.commit()

        return {"message":"Memorable Day deleted successfully!"}

    finally:
        db.close()