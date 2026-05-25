from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from fastapi import FastAPI

from backend.routers import health, expenses, users, dashboard, recurring_expense,income
from backend.database import Base,engine
from backend.models.expense import Expense
from backend.models.user import User
from backend.models.family import Family
from backend.models.recurring_expense import RecurringExpense
from backend.models.income import Income


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(recurring_expense.router)

app.include_router(income.router)
@app.get("/")
def read_root():
    return {"message": "Hello BudgetWise 🚀"}
