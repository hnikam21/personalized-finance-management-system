from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from app.models.income import Income
from app.models.expense import Expense
from app.models.goal import Goal
from app.models.debt import Debt
from app.models.investment import Investment


def calculate_health_score(db: Session, user_id: int, user_type: str) -> float:
    """
    Returns a financial health score between 0 and 100.
    """

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
        return 0.0

    savings = max(total_income - total_expense, 0)
    savings_rate = savings / total_income

    score = 0.0

    # ---------------- SAVINGS SCORE (30) ----------------

    if savings_rate >= 0.30:
        score += 30
    elif savings_rate >= 0.15:
        score += 20
    else:
        score += 10

    # ---------------- GOAL PROGRESS (20) ----------------

    goals = db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.target_amount > 0
    ).all()

    if goals:
        progress_values = [
            float(g.saved_amount) / float(g.target_amount)
            for g in goals
        ]
        avg_progress = sum(progress_values) / len(progress_values)
        score += min(avg_progress * 20, 20)

    # ---------------- USER TYPE LOGIC ----------------

    if user_type == "dependent":
        # Expense discipline (30)
        expense_ratio = total_expense / total_income
        if expense_ratio <= 0.7:
            score += 30
        else:
            score += 15

    else:
        # Independent user logic

        total_debt = db.query(
            func.coalesce(func.sum(Debt.principal_amount), 0)
        ).filter(Debt.user_id == user_id).scalar()

        total_investment = db.query(
            func.coalesce(func.sum(Investment.amount), 0)
        ).filter(Investment.user_id == user_id).scalar()

        total_debt = float(total_debt)
        total_investment = float(total_investment)

        debt_ratio = total_debt / total_income
        investment_ratio = total_investment / total_income

        # Debt score (30)
        if debt_ratio < 0.3:
            score += 30
        elif debt_ratio < 0.5:
            score += 15

        # Investment score (20)
        if investment_ratio >= 0.2:
            score += 20
        elif investment_ratio >= 0.1:
            score += 10

    return round(min(score, 100), 2)
