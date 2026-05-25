from backend.database import SessionLocal
from backend.models.income import Income
from sqlalchemy import func
from decimal import Decimal
from fastapi import HTTPException


def add_income(income_data,user_id):

    db = SessionLocal()
    try:
        db_income = Income(
            amount= Decimal(income_data.amount),
            category=income_data.category,
            frequency=income_data.frequency,
            notes=income_data.notes,
            user_id=user_id,
        )

        db.add(db_income)
        db.commit()
        db.refresh(db_income)

        return {
            "data": db_income,
            "message": "Income added successfully"
        }

    finally:
        db.close()

def get_incomes_by_user_id(user_id):

    db = SessionLocal()

    try:
        db_total_incomes_amount = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).scalar()
        db_categorized_incomes_total = (db.query(Income.category,func.sum(Income.amount))
                                    .filter(Income.user_id == user_id).group_by(Income.category).all())
        db_incomes_details = db.query(Income).filter(Income.user_id == user_id).all()

        categorized_incomes_total = []

        for category in db_categorized_incomes_total:
            categorized_incomes_total.append(
                {
                    "category" : category[0],
                    "total_amount" : category[1]
                }

            )


        return {
            "total_income_amount": db_total_incomes_amount or 0.00,
            "categorized_income_total": categorized_incomes_total or [],
            "incomes_details": db_incomes_details or []
        }

    finally:
        db.close()


def patch_income(income_id,income_update_data,user_id):

    db = SessionLocal()

    try:
        existing_income = (db.query(Income).filter(Income.id == income_id)
                           .filter(Income.user_id == user_id).first())

        if not existing_income:
            raise HTTPException(status_code=404, detail="Income not found or not belongs to this user")

        update_data = income_update_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_income, field, value)

        db.commit()
        db.refresh(existing_income)

        return {
            "data": existing_income,
            "message": "Income updated successfully"
        }

    finally:
        db.close()

def delete_income(income_id,user_id):

    db = SessionLocal()

    try:

        existing_income = db.query(Income).filter(Income.id == income_id).filter(Income.user_id == user_id).first()

        if not existing_income:
            raise HTTPException(status_code=404, detail="Income not found or not belongs to this user")

        db.delete(existing_income)
        db.commit()

        return {"message": "Income deleted successfully"}

    finally:
        db.close()