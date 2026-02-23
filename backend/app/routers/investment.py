from datetime import date
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentResponse, SellInvestmentRequest
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User

from app.services.portfolio_service import update_user_portfolio

router = APIRouter(
    prefix="/investment",
    tags=["Investment"]
)

# ---------------- CREATE INVESTMENT ----------------

@router.post("", response_model=InvestmentResponse)
def add_investment(
    investment: InvestmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    principal = investment.principal_amount

    # Auto calculate for STOCK
    if investment.investment_type == "STOCK":
        principal = investment.quantity * investment.buy_price

    new_investment = Investment(
        user_id=current_user.id,
        investment_type=investment.investment_type,
        principal_amount=principal,
        rate_of_return=investment.rate_of_return,
        quantity=investment.quantity,
        buy_price=investment.buy_price,
        start_date=investment.start_date,
        auto_update=investment.auto_update
    )

    db.add(new_investment)
    db.commit()
    db.refresh(new_investment)

    return new_investment



# ---------------- LIST INVESTMENTS ----------------

@router.get(
    "",
    response_model=List[InvestmentResponse]
)
def list_investments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Investment).filter(
        Investment.user_id == current_user.id
    ).all()

# ---------------- GET PORTFOLIO VALUE ----------------

@router.get("/portfolio")
def get_portfolio(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return update_user_portfolio(db, user.id)

@router.post("/sell/{investment_id}")
def sell_investment(
    investment_id: int,
    payload: SellInvestmentRequest,   # ✅ body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    investment = db.query(Investment).filter(
        Investment.id == investment_id,
        Investment.user_id == current_user.id,
        Investment.is_active == True
    ).first()

    if not investment:
        raise HTTPException(status_code=404, detail="Active investment not found")

    sell_price = payload.sell_price

    investment.sell_price = sell_price
    investment.sell_date = date.today()
    investment.realized_profit = (sell_price - investment.buy_price) * investment.quantity
    investment.is_active = False

    db.commit()

    return {
        "message": "Investment sold successfully",
        "profit": investment.realized_profit
    }
