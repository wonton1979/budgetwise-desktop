from backend.database import SessionLocal
from backend.models.expense import Expense

def add_expense(expense):
    db = SessionLocal()
    try:
        db_expense = Expense(
            amount=expense.amount,
            category=expense.category,
            description=expense.description,
            expense_date=expense.expense_date,
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense
    finally:
        db.close()


def get_expense_by_id(expense_id: int):
    db = SessionLocal()
    try:
        return db.query(Expense).filter(Expense.id == expense_id).first()
    finally:
        db.close()

def delete_expense_by_id(expense_id: int):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()

        if not expense:
            return None

        db.delete(expense)
        db.commit()
        return expense
    finally:
        db.close()

def update_expense_by_id(expense_id:int, expense):
    db = SessionLocal()
    try:
        existing_expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not existing_expense:
            return None
        existing_expense.amount = expense.amount
        existing_expense.category = expense.category
        existing_expense.description = expense.description
        existing_expense.expense_date = expense.expense_date
        db.commit()
        db.refresh(existing_expense)
        return existing_expense
    finally:
        db.close()

def patch_expense_by_id(expense_id: int, expense_data):
    db = SessionLocal()
    try:
        existing_expense = db.query(Expense).filter(Expense.id == expense_id).first()

        if not existing_expense:
            return None

        update_data = expense_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_expense, field, value)

        db.commit()
        db.refresh(existing_expense)

        return existing_expense
    finally:
        db.close()

def get_all_expenses():
    db = SessionLocal()
    try:
        return db.query(Expense).all()
    finally:
        db.close()

