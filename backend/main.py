from fastapi import FastAPI
from backend.routers import health,expenses
from backend.database import Base,engine
from backend.models.expense import Expense

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(health.router)
app.include_router(expenses.router)
@app.get("/")
def read_root():
    return {"message": "Hello BudgetWise 🚀"}
