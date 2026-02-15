from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from app.models.income import Income
from app.models.expense import Expense
from app.models.goal import Goal
from app.models.debt import Debt
from app.models.investment import Investment


def generate_insights(db: Session, user_id: int, user_type: str):
    insights = []

    # ---------------- AGGREGATIONS ----------------

    total_income = db.query(
        func.coalesce(func.sum(Income.amount), 0)
    ).filter(Income.user_id == user_id).scalar()

    total_expense = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(Expense.user_id == user_id).scalar()

    total_income = float(total_income)
    total_expense = float(total_expense)

    if total_income <= 0:
        return [{
            "type": "warning",
            "title": "No income recorded",
            "description": "Please add your income details to receive personalized insights.",
            "impact": "high"
        }]

    savings = max(total_income - total_expense, 0)
    savings_rate = savings / total_income

    # ---------------- SAVINGS INSIGHT ----------------

    if savings_rate < 0.2:
        insights.append({
            "type": "warning",
            "title": "Low savings rate",
            "description": f"You are saving only {int(savings_rate * 100)}% of your income. Aim for at least 20%.",
            "impact": "high"
        })

    # ---------------- SPENDING INSIGHT ----------------

    if total_expense > 0.8 * total_income:
        insights.append({
            "type": "warning",
            "title": "High spending",
            "description": "Your expenses exceed 80% of your income. Consider cutting non-essential expenses.",
            "impact": "high"
        })

    # ---------------- GOAL INSIGHTS ----------------

    goals = db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.target_amount > 0
    ).all()

    for g in goals:
        progress = float(g.saved_amount or 0) / float(g.target_amount)
        if progress < 0.3:
            insights.append({
                "type": "suggestion",
                "title": f"Goal '{g.name}' needs attention",
                "description": "You are behind on this goal. Consider increasing monthly savings.",
                "impact": "medium"
            })

    # ---------------- INDEPENDENT USER INSIGHTS ----------------

    if user_type == "independent":
        total_debt = db.query(
            func.coalesce(func.sum(Debt.principal_amount), 0)
        ).filter(Debt.user_id == user_id).scalar()

        total_investment = db.query(
            func.coalesce(func.sum(Investment.amount), 0)
        ).filter(Investment.user_id == user_id).scalar()

        total_debt = float(total_debt)
        total_investment = float(total_investment)

        if total_debt > 0.5 * total_income:
            insights.append({
                "type": "warning",
                "title": "High debt burden",
                "description": "Your debt exceeds 50% of your income. Consider reducing EMIs or refinancing.",
                "impact": "high"
            })

        if total_investment < 0.15 * total_income:
            insights.append({
                "type": "suggestion",
                "title": "Low investment allocation",
                "description": "You are investing less than 15% of your income. Increasing investments can improve long-term stability.",
                "impact": "medium"
            })

    # Optional: limit insights shown
    return insights[:5]
