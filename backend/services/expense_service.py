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


def get_all_expenses():
    db = SessionLocal()
    try:
        return db.query(Expense).all()
    finally:
        db.close()