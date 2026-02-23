from sqlalchemy.orm import Session
from app.models.investment import Investment
from app.services.investment_engine import update_investment_value

from decimal import Decimal

def update_user_portfolio(db: Session, user_id: int):

    investments = db.query(Investment).filter(
        Investment.user_id == user_id
    ).all()

    total_value = Decimal("0")

    for inv in investments: 

        if not inv.auto_update:
            continue

        new_value = update_investment_value(inv)

        inv.current_value = new_value
        total_value += new_value

    db.commit()

    return {
        "total_portfolio_value": float(total_value),
        "investment_count": len(investments)
    }
