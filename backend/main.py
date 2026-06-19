from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from fastapi import FastAPI

from backend.routers import api_health, expenses, users, dashboard, recurring_expense,income,savings,health,appointment
from backend.database import Base,engine
from backend.models.expense import Expense
from backend.models.user import User
from backend.models.family import Family
from backend.models.recurring_expense import RecurringExpense
from backend.models.income import Income
from backend.models.savings import Savings
from backend.models.health_record import HealthRecord
from backend.models.blood_sugar_record import BloodSugarRecord
from backend.models.blood_pressure_record import BloodPressureRecord
from backend.models.weight_record import WeightRecord
from backend.models.period_record import PeriodRecord
from backend.models.appointment import Appointment


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(api_health.router)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(recurring_expense.router)
app.include_router(income.router)
app.include_router(savings.router)
app.include_router(health.router)
app.include_router(appointment.router)

@app.get("/")
def read_root():
    return {"message": "Hello BudgetWise 🚀"}
