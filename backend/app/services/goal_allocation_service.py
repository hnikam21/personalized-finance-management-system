from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from decimal import Decimal

from app.models.income import Income
from app.models.expense import Expense
from app.models.goal import Goal
from app.models.goal_allocation import GoalAllocation


PRIORITY_WEIGHTS = {
    1: 5,
    2: 4,
    3: 3,
    4: 2,
    5: 1
}


def allocate_monthly_savings(db: Session, user_id: int):

    current_month = datetime.now().month
    current_year = datetime.now().year

    # -----------------------------------------
    # Prevent duplicate allocation
    # -----------------------------------------

    existing = db.query(GoalAllocation).filter(
        GoalAllocation.user_id == user_id,
        GoalAllocation.month == current_month,
        GoalAllocation.year == current_year
    ).first()

    if existing:
        return {"message": "Savings already allocated for this month"}

    # -----------------------------------------
    # Calculate THIS MONTH savings (Decimal safe)
    # -----------------------------------------

    total_income = db.query(
        func.coalesce(func.sum(Income.amount), 0)
    ).filter(
        Income.user_id == user_id,
        extract("month", Income.date) == current_month,
        extract("year", Income.date) == current_year
    ).scalar()

    total_expense = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == user_id,
        extract("month", Expense.date) == current_month,
        extract("year", Expense.date) == current_year
    ).scalar()

    # Ensure Decimal
    total_income = Decimal(total_income or 0)
    total_expense = Decimal(total_expense or 0)

    savings = total_income - total_expense

    if savings <= Decimal("0"):
        return {"message": "No savings available this month"}

    # -----------------------------------------
    # Active goals
    # -----------------------------------------

    goals = db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.target_amount > Goal.saved_amount
    ).all()

    if not goals:
        return {"message": "No active goals"}

    total_weight = sum(
        PRIORITY_WEIGHTS.get(g.priority, 1) for g in goals
    )

    total_weight = Decimal(total_weight)

    # -----------------------------------------
    # Allocate safely
    # -----------------------------------------

    for goal in goals:

        weight = Decimal(PRIORITY_WEIGHTS.get(goal.priority, 1))

        share = (savings * weight) / total_weight

        remaining = Decimal(goal.target_amount) - Decimal(goal.saved_amount or 0)

        allocation = min(share, remaining)

        if allocation > Decimal("0"):

            goal.saved_amount = Decimal(goal.saved_amount or 0) + allocation

            db.add(GoalAllocation(
                user_id=user_id,
                goal_id=goal.id,
                month=current_month,
                year=current_year,
                allocated_amount=allocation
            ))

    db.commit()

    return {"message": "Monthly savings allocated successfully"}
