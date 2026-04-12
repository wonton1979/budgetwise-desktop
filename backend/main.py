from fastapi import FastAPI
from backend.routers import health

app = FastAPI()
app.include_router(health.router)
@app.get("/")
def read_root():
    return {"message": "Hello BudgetWise 🚀"}
