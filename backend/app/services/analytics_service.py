from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict
import json

from app.models.income import Income
from app.models.expense import Expense
from app.db.redis import redis_client

#helper function

def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


# -------------------------------------------------
# MONTHLY FINANCIAL SUMMARY
# -------------------------------------------------

def calculate_monthly_summary(
    db: Session,
    user_id: int,
    month: int,
    year: int
):
    cache_key = f"analytics:summary:{user_id}:{month}:{year}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

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

    result = {
        "income": serialize_value(total_income),
        "expense": serialize_value(total_expense),
        "savings": serialize_value(total_income - total_expense)
    }

    redis_client.setex(cache_key, 300, json.dumps(result))
    return result



# -------------------------------------------------
# CATEGORY-WISE EXPENSE ANALYSIS
# -------------------------------------------------

def category_expense_analysis(
    db: Session,
    user_id: int,
    month: int,
    year: int
):
    cache_key = f"analytics:category:{user_id}:{month}:{year}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    rows = db.query(
        Expense.category_id,
        func.sum(Expense.amount).label("total")
    ).filter(
        Expense.user_id == user_id,
        extract("month", Expense.date) == month,
        extract("year", Expense.date) == year
    ).group_by(
        Expense.category_id
    ).all()

    total_spent = sum(row.total for row in rows) or Decimal(1)

    result = {
        row.category_id: round(float(row.total / total_spent) * 100, 2)
        for row in rows
    }

    redis_client.setex(cache_key, 300, json.dumps(result))
    return result

