from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User
from app.ml.self_learning_classifier import classify_expense


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

    auto_categorized = False
    category_id = expense.category_id

    # ---------------------------------------------
    # 🤖 If no category → Use Self Learning Model
    # ---------------------------------------------
    if not category_id:

        if not expense.description:
            raise HTTPException(
                status_code=400,
                detail="Description required"
            )

        predicted_category, model_source = classify_expense(
            db,
            current_user.id,
            expense.description
        )

        category = db.query(Category).filter(
            Category.name == predicted_category,
            Category.user_id == current_user.id
        ).first()

        if not category:
            raise HTTPException(
                status_code=400,
                detail=f"Predicted category '{predicted_category}' not found"
            )

        category_id = category.id
        auto_categorized = True

    # Manual category validation
    else:
        category = db.query(Category).filter(
            Category.id == category_id,
            Category.user_id == current_user.id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    new_expense = Expense(
        user_id=current_user.id,
        category_id=category_id,
        amount=expense.amount,
        date=expense.date,
        description=expense.description,
        auto_categorized=auto_categorized
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

    summary: dict[int, Decimal] = {}

    for e in expenses:
        summary[e.category_id] = summary.get(e.category_id, Decimal("0")) + e.amount

    return summary
