from backend.database import SessionLocal
from backend.models.recurring_expense import RecurringExpense
from backend.models.recurring_expense_category import RecurringExpenseCategory
from backend.models.recurring_expense_subcategory import RecurringSubcategory
from fastapi import HTTPException
from sqlalchemy import func

ALLOWED_RECURRING_SUBCATEGORIES = {

    RecurringExpenseCategory.HOUSING: [
        RecurringSubcategory.MORTGAGE,
        RecurringSubcategory.RENT,
        RecurringSubcategory.COUNCIL_TAX,
        RecurringSubcategory.HOME_INSURANCE,
    ],

    RecurringExpenseCategory.UTILITIES: [
        RecurringSubcategory.ELECTRICITY,
        RecurringSubcategory.GAS,
        RecurringSubcategory.WATER,
        RecurringSubcategory.BROADBAND,
        RecurringSubcategory.MOBILE_BILL,
        RecurringSubcategory.TV_LICENCE,
    ],

    RecurringExpenseCategory.INSURANCE: [
        RecurringSubcategory.CAR_INSURANCE,
        RecurringSubcategory.LIFE_INSURANCE,
        RecurringSubcategory.PET_INSURANCE,
        RecurringSubcategory.HOME_EMERGENCY,
        RecurringSubcategory.BREAKDOWN_COVER,
        RecurringSubcategory.PHONE_INSURANCE,
    ],

    RecurringExpenseCategory.SUBSCRIPTION: [
        RecurringSubcategory.STREAMING,
        RecurringSubcategory.TV_PACKAGE,
        RecurringSubcategory.GAMING_SUBSCRIPTION,
        RecurringSubcategory.SOFTWARE_SUBSCRIPTION,
    ],

    RecurringExpenseCategory.HEALTHCARE: [
        RecurringSubcategory.MEDICAL,
        RecurringSubcategory.DENTAL,
        RecurringSubcategory.EYE_CARE,
        RecurringSubcategory.PRESCRIPTION,
    ],

    RecurringExpenseCategory.TRANSPORT: [
        RecurringSubcategory.PARKING,
        RecurringSubcategory.FUEL,
        RecurringSubcategory.TRANSPORT_PASS,
        RecurringSubcategory.CAR_FINANCE,
        RecurringSubcategory.ROAD_TAX,
    ],

    RecurringExpenseCategory.OTHER: [
        RecurringSubcategory.OTHER,
    ],
}

def add_recurring_expense(expense_data,user_id):

    db = SessionLocal()

    validate_category_subcategory(expense_data.category,expense_data.subcategory)

    try:
        db_recurring_expense = RecurringExpense(
            amount=expense_data.amount,
            category=expense_data.category,
            subcategory=expense_data.subcategory,
            provider_name=expense_data.provider_name,
            frequency=expense_data.frequency,
            payment_method=expense_data.payment_method,
            start_date=expense_data.start_date,
            end_date=expense_data.end_date,
            is_public_to_family=expense_data.is_public_to_family,
            notes=expense_data.notes,
            user_id=user_id
        )

        db.add(db_recurring_expense)
        db.commit()
        db.refresh(db_recurring_expense)
        return db_recurring_expense
    finally:
        db.close()

def get_recurring_expenses_by_user_id(user_id):

    db = SessionLocal()

    try:

        db_recurring_expense = db.query(RecurringExpense).filter(RecurringExpense.user_id == user_id).order_by(RecurringExpense.category.asc()).all()

        db_category_summary = (db.query(RecurringExpense.category, func.sum(RecurringExpense.amount).label("amount"))
                               .filter(RecurringExpense.user_id == user_id)
                               .group_by(RecurringExpense.category).order_by(RecurringExpense.category.asc()).all())


        if not db_recurring_expense:
            raise HTTPException(status_code=404, detail="Expense not found or not belongs to this user")

        category_summary = []


        for category, amount in db_category_summary:
            expenses_list = []
            for each_expense in db_recurring_expense:
                if each_expense.category == category:
                    expenses_list.append(each_expense)

            category_summary.append(
                {
                    "category": category,
                    "total_amount": amount,
                    "expenses": expenses_list
                 }
            )

        return {
            "data": category_summary,
            "message": "Retrieving recurring expenses successfully",
        }

    finally:
        db.close()

def update_recurring_expense(expense_id, update_data, user_id):

    db = SessionLocal()

    validate_category_subcategory(update_data.category, update_data.subcategory)

    try:
        existing_recurring_expense = (db.query(RecurringExpense).filter(RecurringExpense.id==expense_id)
                             .filter(RecurringExpense.user_id == user_id).first())

        if not existing_recurring_expense:
            raise HTTPException(status_code=404, detail="Expense not found or not belongs to this user")

        update_data = update_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_recurring_expense, field, value)

        db.commit()
        db.refresh(existing_recurring_expense)
        return existing_recurring_expense

    finally:
        db.close()


def delete_recurring_expense(expense_id, user_id):

    db = SessionLocal()

    try:
        existing_recurring_expense = (db.query(RecurringExpense).filter(RecurringExpense.id==expense_id)
                             .filter(RecurringExpense.user_id == user_id).first())

        if not existing_recurring_expense:
            raise HTTPException(status_code=404, detail="Expense not found or not belongs to this user")

        db.delete(existing_recurring_expense)
        db.commit()

        return {"message": "Recurring expense deleted successfully"}

    finally:
        db.close()


def validate_category_subcategory(category, subcategory):

    allowed_subcategories = ALLOWED_RECURRING_SUBCATEGORIES.get(category)

    if not allowed_subcategories or subcategory not in allowed_subcategories:
        raise ValueError("Invalid subcategory for selected category")