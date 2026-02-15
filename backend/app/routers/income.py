from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


# ---------------- ADD INCOME ----------------

@router.post(
    "",
    response_model=IncomeResponse,
    status_code=status.HTTP_201_CREATED
)
def add_income(
    income: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_income = Income(
        user_id=current_user.id,
        source=income.source,
        amount=income.amount,
        date=income.date,
        recurring=income.recurring
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income


# ---------------- MONTHLY INCOME ----------------

@router.get("/monthly")
def get_monthly_income(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incomes = db.query(Income).filter(
        Income.user_id == current_user.id
    ).all()

    total = sum((i.amount for i in incomes), Decimal("0"))

    return {
        "total_income": total,
        "records": incomes
    }
