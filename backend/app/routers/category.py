from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


# ---------------- ADD CATEGORY ----------------

from fastapi import HTTPException

@router.post("/")
def add_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    existing = db.query(Category).filter(
        Category.name == category.name,
        Category.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        name=category.name,
        user_id=current_user.id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category 
