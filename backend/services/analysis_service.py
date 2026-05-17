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
            func.sum(Expense.amount),
            func.count(Expense.id)
        ).filter(Expense.user_id == user_id).filter(
            and_(
                Expense.expense_date >= date(int(year_to_analyse), int(month_to_analyse), 1)),
            Expense.expense_date <= date(int(year_to_analyse), int(month_to_analyse), days_in_month[1])
        ).first()

        sum_expense = analysis_result[0]
        count_expense = analysis_result[1]

        highest_single_transaction = (
            db.query(Expense)
            .filter(Expense.user_id == user_id)
            .filter(
               Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 1), date(int(year_to_analyse), int(month_to_analyse), days_in_month[1]))
            )
            .order_by(Expense.amount.desc())
            .first()
        )

        highest_category = db.query(
            Expense.category,
            func.sum(Expense.amount)
        ).filter(Expense.user_id == user_id).group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).first()

        current_day = int(date.today().strftime("%d"))

        return {

                "total_expenses": sum_expense,
                "transaction_count": count_expense,
                "top_category": highest_category[0] if highest_category else None,
                "top_category_amount": highest_category[1] if highest_category else 0,
                "highest_expense": highest_single_transaction.amount if highest_single_transaction else 0,
                "highest_expense_shop": highest_single_transaction.shop_name if highest_single_transaction else None,
                "highest_expense_date": highest_single_transaction.expense_date if highest_single_transaction else None,
                "average_daily_spending": round(sum_expense / current_day, 2),
        }

    finally:
        db.close()

