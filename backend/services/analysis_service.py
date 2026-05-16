from backend.database import SessionLocal
from backend.models.expense import Expense
from sqlalchemy import func, and_
import calendar
from datetime import date


def monthly_expense_analysis(year_to_analyse,month_to_analyse,user_id):
    db=SessionLocal()
    try:
        days_in_month = calendar.monthrange(int(year_to_analyse), int(month_to_analyse))
        analysis_result = db.query(
            func.max(Expense.amount),
            func.sum(Expense.amount),
            func.avg(Expense.amount),
            func.count(Expense.id)
        ).filter(Expense.user_id == user_id).filter(
            and_(
                Expense.expense_date >= date(int(year_to_analyse), int(month_to_analyse), 1)),
            Expense.expense_date <= date(int(year_to_analyse), int(month_to_analyse), days_in_month[1])
        ).first()

        max_expense = analysis_result[0]
        sum_expense = analysis_result[1]
        avg_expense = analysis_result[2]
        count_expense = analysis_result[3]

        highest_category = db.query(
            Expense.category,
            func.sum(Expense.amount)
        ).filter(Expense.user_id == user_id).group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).first()

        return {

                "total_expenses": sum_expense,
                "transaction_count": count_expense,
                "top_category": highest_category[0] if highest_category else None,
                "top_category_amount": highest_category[1] if highest_category else 0,
                "highest_expense": max_expense,
                "average_daily_spending": avg_expense,
        }

    finally:
        db.close()

