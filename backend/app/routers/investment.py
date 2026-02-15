from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/investment",
    tags=["Investment"]
)

# ---------------- CREATE INVESTMENT ----------------

@router.post(
    "",
    response_model=InvestmentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_investment(
    investment: InvestmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_investment = Investment(
        user_id=current_user.id,
        investment_type=investment.investment_type,
        amount=investment.amount,
        expected_return=investment.expected_return,
        start_date=investment.start_date
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
    investments = db.query(Investment).filter(
        Investment.user_id == current_user.id
    ).all()

    return investments
