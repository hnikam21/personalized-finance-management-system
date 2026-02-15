from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.models.debt import Debt
from app.schemas.debt import DebtCreate, DebtResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/debt",
    tags=["Debt"]
)

# ---------------- CREATE DEBT ----------------

@router.post(
    "",
    response_model=DebtResponse,
    status_code=status.HTTP_201_CREATED
)
def add_debt(
    debt: DebtCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_debt = Debt(
        user_id=current_user.id,
        debt_type=debt.debt_type,
        principal_amount=debt.principal_amount,
        interest_rate=debt.interest_rate,
        due_date=debt.due_date
    )

    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)

    return new_debt


# ---------------- LIST DEBTS ----------------

@router.get(
    "",
    response_model=List[DebtResponse]
)
def list_debts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    debts = db.query(Debt).filter(
        Debt.user_id == current_user.id
    ).all()

    return debts
