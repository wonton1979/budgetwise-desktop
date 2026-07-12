from backend.database import SessionLocal
from backend.models.savings import Savings
from backend.utils.current_user_exchange_rate import get_current_user_exchange_rate
from decimal import Decimal


def add_savings(savings_data,user_id):

    db = SessionLocal()

    try:
        new_savings = Savings(
            user_id=user_id,
            goal_amount=savings_data.goal_amount,
            current_amount=savings_data.current_amount,
            purpose_name=savings_data.purpose_name,
            target_date=savings_data.target_date,
            notes=savings_data.notes,
        )

        db.add(new_savings)
        db.commit()
        db.refresh(new_savings)
        return {"message": "New savings added successfully"}

    finally:
        db.close()

def get_all_savings_by_user_id(user_id):

    db = SessionLocal()

    try:
        db_existing_savings = db.query(Savings).filter(Savings.user_id == user_id).all()

        existing_savings = []

        exchange_rate = Decimal(get_current_user_exchange_rate(user_id))

        for savings in db_existing_savings:

            existing_savings.append(
                {
                    "id": savings.id,
                    "goal_amount": round(savings.goal_amount * exchange_rate, 2),
                    "current_amount": round(savings.current_amount * exchange_rate, 2),
                    "purpose_name": savings.purpose_name,
                    "target_date": savings.target_date,
                    "notes": savings.notes,
                }
            )

        return {
            "data": existing_savings,
            "message": "Savings data retrieved successfully"
        }

    finally:
        db.close()

def get_savings_by_id(user_id, savings_id):

    db = SessionLocal()

    try:
        db_existing_savings = db.query(Savings).filter(Savings.user_id == user_id).filter(Savings.id==savings_id).first()

        if not db_existing_savings:
            return {
                "message": "Savings not found"
            }


        existing_savings ={
                "id": db_existing_savings.id,
                "goal_amount": db_existing_savings.goal_amount,
                "current_amount": db_existing_savings.current_amount,
                "purpose_name": db_existing_savings.purpose_name,
                "target_date": db_existing_savings.target_date,
                "notes": db_existing_savings.notes,
            }

        return {
            "data": existing_savings,
            "message": "Savings data retrieved successfully"
        }

    finally:
        db.close()


def update_savings(user_id, savings_id,savings_data):

    db = SessionLocal()

    try:
        existing_savings = db.query(Savings).filter(Savings.user_id == user_id).filter(Savings.id==savings_id).first()

        if not existing_savings:
            return {
                "message": "Updated Failed,Savings not found"
            }

        savings_data = savings_data.model_dump(exclude_unset=True)

        for field, value in savings_data.items():
            setattr(existing_savings, field, value)

        db.commit()
        db.refresh(existing_savings)

        return {"message": "Savings updated successfully"}

    finally:
        db.close()


def delete_savings(user_id, savings_id):

    db = SessionLocal()

    try:
        existing_savings = db.query(Savings).filter(Savings.user_id == user_id).filter(Savings.id == savings_id).first()

        if not existing_savings:
            return {
                "message": "Delete Savings Failed,Savings not found"
            }

        db.delete(existing_savings)
        db.commit()
        return {
            "message": "Savings deleted successfully"
        }
    finally:
        db.close()


