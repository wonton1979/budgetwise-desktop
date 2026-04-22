from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__),"..", ".env"))

from fastapi import FastAPI

from backend.routers import health, expenses, users
from backend.database import Base,engine
from backend.models.expense import Expense
from backend.models.user import User
from backend.models.family import Family


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(expenses.router)

app.include_router(users.router)
@app.get("/")
def read_root():
    return {"message": "Hello BudgetWise 🚀"}
