from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.dependencies import get_db
from app.models.category import Category
from app.constants.default_categories import DEFAULT_CATEGORIES


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# OAuth2 scheme (used later for protected routes)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ------------------- REGISTER -------------------

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        user_type=user_data.user_type,
        monthly_income=user_data.monthly_income,
        risk_profile=user_data.risk_profile,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create default categories for the new user
    for category_name in DEFAULT_CATEGORIES:
        category = Category(
            name=category_name,
            user_id=new_user.id
        )
        db.add(category)

    db.commit()
    return new_user


# ------------------- LOGIN -------------------

@router.post(
    "/login",
    response_model=Token
)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(
        credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
