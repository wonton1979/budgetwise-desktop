from fastapi import FastAPI
from backend.routers import health,expenses

app = FastAPI()
app.include_router(health.router)
app.include_router(expenses.router)
@app.get("/")
def read_root():
    return {"message": "Hello BudgetWise 🚀"}
