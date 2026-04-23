from backend.database import SessionLocal
from backend.models.expense import Expense
from backend.models.order import Order
from backend.models.sort_by import SortBy
from fastapi import HTTPException

def add_expense(expense,current_user_id):
    db = SessionLocal()
    try:
        db_expense = Expense(
            amount=expense.amount,
            category=expense.category,
            description=expense.description,
            expense_date=expense.expense_date,
            user_id=current_user_id,
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense
    finally:
        db.close()


def get_expense_by_id(expense_id: int,user_id):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).filter(Expense.user_id == user_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found or not belongs to this user")
        return expense
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

def update_expense_by_id(expense_id:int, expense,user_id):
    db = SessionLocal()
    try:
        existing_expense = db.query(Expense).filter(Expense.id == expense_id).filter(Expense.user_id==user_id).first()
        if not existing_expense:
            raise HTTPException(status_code=404, detail="Expense not found or not belongs to this user")
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

def get_all_expenses(category,min_amount,max_amount,start_date,end_date,sort_by,order,page,limit,user_id):
    db = SessionLocal()
    total = 0
    try:
        if (page is None and limit is not None) or (page is not None and limit is None):
            raise HTTPException(status_code=400, detail="page and limit must be used together")

        if page is not None and page < 1:
            raise HTTPException(status_code=400, detail="page must be >= 1")

        if limit is not None and limit < 1:
            raise HTTPException(status_code=400, detail="limit must be >= 1")
        query = db.query(Expense).filter(Expense.user_id == user_id)
        if category:
            query = query.filter(Expense.category == category)
        if min_amount is not None:
            query = query.filter(Expense.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Expense.amount <= max_amount)
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)
        total = query.count()
        if sort_by:
            if sort_by == SortBy.EXPENSE_DATE:
                sort_column = Expense.expense_date
                if order == Order.DESC:
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())
            if sort_by == SortBy.AMOUNT:
                sort_column = Expense.amount
                if order == Order.DESC:
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())
        if page is not None and limit is not None:
            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit)

        return {
            "data":query.all(),
            "total":total,
            "page":page,
            "limit":limit,
        }
    finally:
        db.close()

