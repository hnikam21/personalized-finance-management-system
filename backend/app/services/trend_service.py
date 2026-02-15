from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.income import Income
from app.models.expense import Expense


def get_monthly_trend(db: Session, user_id: int, year: int):

    trend_data = []

    for month in range(1, 13):

        total_income = db.query(
            func.coalesce(func.sum(Income.amount), 0)
        ).filter(
            Income.user_id == user_id,
            extract("month", Income.date) == month,
            extract("year", Income.date) == year
        ).scalar()

        total_expense = db.query(
            func.coalesce(func.sum(Expense.amount), 0)
        ).filter(
            Expense.user_id == user_id,
            extract("month", Expense.date) == month,
            extract("year", Expense.date) == year
        ).scalar()

        total_income = float(total_income)
        total_expense = float(total_expense)

        trend_data.append({
            "month": month,
            "income": total_income,
            "expense": total_expense,
            "savings": total_income - total_expense
        })

    return trend_data
