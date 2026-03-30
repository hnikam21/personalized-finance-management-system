from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/expense",
    tags=["Expense"]
)

# ---------------- ADD EXPENSE ----------------

@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ❌ Removed ML logic completely
    # ✅ Only manual category allowed

    category = db.query(Category).filter(
        Category.id == expense.category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_expense = Expense(
        user_id=current_user.id,
        category_id=expense.category_id,
        amount=expense.amount,
        date=expense.date,
        description=expense.description,
        auto_categorized=False   # always false now
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# ---------------- EXPENSE SUMMARY ----------------

@router.get("/summary")
def expense_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()

    total_expense = sum((e.amount for e in expenses), Decimal("0"))

    category_breakdown = {}

    for e in expenses:
        category = db.query(Category).filter(Category.id == e.category_id).first()
        if category:
            category_name = category.name
            category_breakdown[category_name] = (
                category_breakdown.get(category_name, Decimal("0")) + e.amount
            )

    return {
        "total_expense": float(total_expense),
        "category_breakdown": {
            k: float(v) for k, v in category_breakdown.items()
        }
    }


# ---------------- RECENT EXPENSES ----------------

@router.get("/")
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expenses = (
        db.query(Expense, Category.name.label("category"))
        .join(Category, Expense.category_id == Category.id)
        .filter(Expense.user_id == current_user.id)
        .order_by(Expense.date.desc())
        .limit(10)
        .all()
    )

    result = []
    for expense, category_name in expenses:
        result.append({
            "id": expense.id,
            "amount": float(expense.amount),
            "date": expense.date,
            "description": expense.description,
            "category": category_name,
            "auto_categorized": expense.auto_categorized
        })

    return {"expenses": result}