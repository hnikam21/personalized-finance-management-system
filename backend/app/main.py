from fastapi import FastAPI
from app.routers import auth, income, expense, goal, category, insights, investment, debt, health, alert
from app.core.scheduler import start_scheduler


app = FastAPI(title="Personalized Finance Management System")


app.include_router(auth.router)
app.include_router(income.router)
app.include_router(expense.router)
app.include_router(category.router)
app.include_router(goal.router)
app.include_router(insights.router)
app.include_router(investment.router)
app.include_router(debt.router)
app.include_router(health.router)
app.include_router(alert.router)


@app.get("/")
def root():
    return {"message": "Finance Management API running"}

# @app.on_event("startup")
# def startup_event():
#     start_scheduler()



