from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.expense import Expense
from app.models.category import Category
from app.models.goal import Goal
from app.models.debt import Debt
from app.models.alert import Alert, AlertSeverity


def generate_alerts(db: Session, user_id: int):
    alerts_to_create = []

    # --------------------------------------------------
    # 1️⃣ Budget exceeded alerts (SQL aggregation)
    # --------------------------------------------------

    budgets = db.query(
        Category.id,
        Category.name,
        Category.budget_limit,
        func.coalesce(func.sum(Expense.amount), 0).label("spent")
    ).outerjoin(
        Expense,
        Expense.category_id == Category.id
    ).filter(
        Category.user_id == user_id,
        Category.budget_limit.isnot(None)
    ).group_by(
        Category.id
    ).all()

    for cat_id, name, limit, spent in budgets:
        if spent > limit:
            exists = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == "BUDGET_EXCEEDED",
                Alert.message == f"Budget exceeded for {name}",
                Alert.is_read == False
            ).first()

            if not exists:
                alerts_to_create.append(Alert(
                    user_id=user_id,
                    alert_type="BUDGET_EXCEEDED",
                    message=f"Budget exceeded for {name}",
                    severity=AlertSeverity.high
                ))

    # --------------------------------------------------
    # 2️⃣ Goal deviation alerts
    # --------------------------------------------------

    goals = db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.deadline.isnot(None),
        Goal.target_amount > 0
    ).all()

    for g in goals:
        progress = float(g.saved_amount or 0) / float(g.target_amount)

        days_left = (g.deadline - date.today()).days
        if days_left <= 0:
            continue

        if progress < 0.3:
            exists = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == "GOAL_DEVIATION",
                Alert.message == f"Goal '{g.name}' is behind schedule",
                Alert.is_read == False
            ).first()

            if not exists:
                alerts_to_create.append(Alert(
                    user_id=user_id,
                    alert_type="GOAL_DEVIATION",
                    message=f"Goal '{g.name}' is behind schedule",
                    severity=AlertSeverity.medium
                ))

    # --------------------------------------------------
    # 3️⃣ EMI / Debt reminders
    # --------------------------------------------------

    upcoming_date = date.today() + timedelta(days=7)

    debts = db.query(Debt).filter(
        Debt.user_id == user_id,
        Debt.due_date <= upcoming_date
    ).all()

    for d in debts:
        exists = db.query(Alert).filter(
            Alert.user_id == user_id,
            Alert.alert_type == "EMI_REMINDER",
            Alert.message == f"Upcoming EMI for {d.debt_type}",
            Alert.is_read == False
        ).first()

        if not exists:
            alerts_to_create.append(Alert(
                user_id=user_id,
                alert_type="EMI_REMINDER",
                message=f"Upcoming EMI for {d.debt_type}",
                severity=AlertSeverity.high
            ))

    # --------------------------------------------------
    # SAVE ALL ALERTS
    # --------------------------------------------------

    if alerts_to_create:
        db.add_all(alerts_to_create)
        db.commit()
