from sqlalchemy import and_

from datetime import datetime,UTC
from fastapi import HTTPException

from backend.models.family import Family
from backend.utils.family_code_generator import generate_family_code
from backend.database import SessionLocal
from backend.models.expense import Expense
from backend.models.order import Order
from backend.models.sort_by import SortBy
from backend.models.user import User
from backend.models.recurring_expense import RecurringExpense

from decimal import Decimal
from backend.utils.current_user_exchange_rate import get_current_user_exchange_rate


def add_family(username):
    db = SessionLocal()
    try:
        db_family = Family(
            family_name="family_" + username,
            family_code=generate_family_code(),
            created_at=datetime.now(UTC),
        )
        db.add(db_family)
        db.commit()
        db.refresh(db_family)
        return db_family

    finally:
        db.close()

def get_family_by_family_code(family_code):
    db = SessionLocal()
    try:
        db_family = db.query(Family).filter_by(family_code=family_code).first()
        if not db_family:
            raise HTTPException(status_code=404, detail="No family was found with the provided family code.\n\n"
                                                        "Please check the code and try again.")
        return db_family
    finally:
        db.close()

def get_family_by_family_id(family_id):

    db = SessionLocal()
    try:
        db_family = db.query(Family).filter_by(id=family_id).first()
        if not db_family:
            raise HTTPException(status_code=404, detail="Family not found")
        return db_family
    finally:
        db.close()


def get_all_family_expenses(category,min_amount,max_amount,start_date,end_date,sort_by,order,page,limit,current_user):
    db = SessionLocal()
    exchange_rate = Decimal(get_current_user_exchange_rate(current_user.id))
    try:
        if (page is None and limit is not None) or (page is not None and limit is None):
            raise HTTPException(status_code=400, detail="page and limit must be used together")

        if page is not None and page < 1:
            raise HTTPException(status_code=400, detail="page must be >= 1")

        if limit is not None and limit < 1:
            raise HTTPException(status_code=400, detail="limit must be >= 1")

        query = (
            db.query(Expense,User.display_name)
            .join(User, Expense.user_id == User.id)
            .filter(
                    and_(
                        User.family_id == current_user.family_id,
                        Expense.is_public_to_family.is_(True),
                        User.id != current_user.id
                )
            )
        )

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
        else:
            sort_column = Expense.expense_date
            query = query.order_by(sort_column.desc())

        if page is not None and limit is not None:
            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit)

        results = query.all()

        data = []

        for expense, display_name in results:
            data.append({
                "id": expense.id,
                "amount": round(expense.amount * exchange_rate, 2),
                "category": expense.category,
                "shop_name": expense.shop_name,
                "shopping_type": expense.shopping_type,
                "payment_method": expense.payment_method,
                "tag": expense.tag,
                "expense_date": expense.expense_date,
                "notes": expense.notes,
                "is_public_to_family": expense.is_public_to_family,
                "display_name": display_name,
            })

        return {
            "data":data,
            "total":total,
            "page":page,
            "limit":limit,
        }
    finally:
        db.close()

def get_all_family_recurring_expenses(current_user,category=None,start_date=None,end_date=None,sort_by=None,order=None,page=None,limit=None):

    db = SessionLocal()
    exchange_rate = Decimal(get_current_user_exchange_rate(current_user.id))
    try:
        db_family_recurring_expenses = (db.query(RecurringExpense,User.display_name,User.username)
        .join(User, RecurringExpense.user_id == User.id).filter(
                    and_(
                        User.family_id == current_user.family_id,
                        RecurringExpense.is_public_to_family.is_(True),
                )
            )).all()

        family_recurring_expenses = []

        for each_family_recurring_expense, display_name, username in db_family_recurring_expenses:

            if display_name:
                owner= display_name
            else:
                owner = username

            family_recurring_expenses.append(
                {
                    "owner": owner,
                    "provider_name": each_family_recurring_expense.provider_name,
                    "amount": round(each_family_recurring_expense.amount * exchange_rate, 2),
                    "subcategory": each_family_recurring_expense.subcategory,
                    "frequency": each_family_recurring_expense.frequency,
                    "notes": each_family_recurring_expense.notes,
                }
            )

        return {
            "data": family_recurring_expenses,
            "total": len(family_recurring_expenses),
            "message": "Recurring expenses successfully retrieved",
        }

    finally:
        db.close()

