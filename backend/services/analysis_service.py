from backend.database import SessionLocal
from backend.models.expense import Expense
from backend.models.income import Income
from backend.models.frequency import Frequency
from backend.models.recurring_expense import RecurringExpense
from sqlalchemy import func, and_,or_
from decimal import Decimal
import calendar
from datetime import date

from backend.utils.current_user_exchange_rate import get_current_user_exchange_rate


def monthly_analysis_for_dashboard(year_to_analyse, month_to_analyse, user_id):
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

        highest_category = (db.query(
            Expense.category,
            func.sum(Expense.amount)
        ).filter(Expense.user_id == user_id).filter(
               Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 1),
                                            date(int(year_to_analyse), int(month_to_analyse), days_in_month[1]))
            ).group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).first())

        current_day = int(date.today().strftime("%d"))

        db_recurring_incomes_total = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).filter(
            Income.frequency != Frequency.ONE_OFF).scalar()

        db_one_off_incomes_total = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).filter(
            Income.frequency == Frequency.ONE_OFF).filter(
            Income.received_date.between(date(int(year_to_analyse), int(month_to_analyse), 1),
                                         date(int(year_to_analyse), int(month_to_analyse), days_in_month[1]))
        ).scalar() or Decimal(0)

        incomes_total = 0

        if db_one_off_incomes_total and db_recurring_incomes_total:
            incomes_total = db_one_off_incomes_total + db_recurring_incomes_total
            
        if db_recurring_incomes_total and not db_one_off_incomes_total:
            incomes_total = db_recurring_incomes_total

        db_recurring_expenses = db.query(func.sum(RecurringExpense.amount)).filter(
            RecurringExpense.user_id == user_id).filter(
            or_(RecurringExpense.end_date.is_(None),
                RecurringExpense.end_date >= date(int(year_to_analyse), int(month_to_analyse), 1))).scalar()

        exchange_rate = Decimal(get_current_user_exchange_rate(user_id))

        return {

                "total_expenses": sum_expense * exchange_rate if sum_expense else 0.00,
                "transaction_count": count_expense if count_expense else 0,
                "top_category": highest_category[0] if highest_category else "N/A",
                "top_category_amount": round(highest_category[1] * exchange_rate,2) if highest_category else 0,
                "highest_expense": round(highest_single_transaction.amount * exchange_rate,2) if highest_single_transaction else 0,
                "highest_expense_shop": highest_single_transaction.shop_name if highest_single_transaction else "N/A",
                "highest_expense_date": highest_single_transaction.expense_date if highest_single_transaction else "N/A",
                "average_daily_spending": round((sum_expense / current_day)* exchange_rate, 2)  if sum_expense else 0.00,
                "total_incomes": incomes_total * exchange_rate if incomes_total else 0.00,
                "total_recurring_expenses": db_recurring_expenses * exchange_rate if db_recurring_expenses else 0.00,
        }

    finally:
        db.close()

def get_weekly_expenses(year_to_analyse,month_to_analyse,user_id):
    db=SessionLocal()
    days_in_month = calendar.monthrange(int(year_to_analyse), int(month_to_analyse))
    exchange_rate = Decimal(get_current_user_exchange_rate(user_id))
    try:
        week_one_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).filter(
            Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 1),
                                         date(int(year_to_analyse), int(month_to_analyse), 7)),
        ).scalar()

        week_two_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).filter(
            Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 8),
                                         date(int(year_to_analyse), int(month_to_analyse), 15)),
        ).scalar()

        week_three_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).filter(
            Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 16),
                                         date(int(year_to_analyse), int(month_to_analyse), 21)),
        ).scalar()

        week_four_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).filter(
            Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 22),
                                         date(int(year_to_analyse), int(month_to_analyse), days_in_month[1])),
        ).scalar()

        week_one_expenses = week_one_expenses or Decimal("0")
        week_two_expenses = week_two_expenses or Decimal("0")
        week_three_expenses = week_three_expenses or Decimal("0")
        week_four_expenses = week_four_expenses or Decimal("0")

        return [
            {"label": "Week 1", "value": round(week_one_expenses * exchange_rate,2) or 0.00},
            {"label": "Week 2", "value": round(week_two_expenses * exchange_rate,2) or 0.00},
            {"label": "Week 3", "value": round(week_three_expenses * exchange_rate,2) or 0.00},
            {"label": "Week 4", "value": round(week_four_expenses * exchange_rate,2) or 0.00},
        ]

    finally:
        db.close()

def category_analysis(year_to_analyse, month_to_analyse, user_id):

    db=SessionLocal()
    days_in_month = calendar.monthrange(int(year_to_analyse), int(month_to_analyse))

    try:
        monthly_total_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).filter(
            Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 1),
                                         date(int(year_to_analyse), int(month_to_analyse), days_in_month[1]))
        ).scalar()

        category_monthly_summary = (db.query(Expense.category, func.sum(Expense.amount))
                                    .filter(Expense.user_id == user_id)
                                    .filter(
            Expense.expense_date.between(date(int(year_to_analyse), int(month_to_analyse), 1),
                                         date(int(year_to_analyse), int(month_to_analyse), days_in_month[1]))
        ).group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).all())

        if not category_monthly_summary or not monthly_total_expenses:
            return []

        category_monthly_summary_list = []

        for category in category_monthly_summary:
            category_monthly_summary_list.append({
                "category": category[0],
                "amount": category[1],
                "percentage": round(category[1] / monthly_total_expenses * 100, 2),
            })

        return category_monthly_summary_list
    finally:
        db.close()



