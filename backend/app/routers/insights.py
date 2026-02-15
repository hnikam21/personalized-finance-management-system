from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User
from app.services.analytics_service import (
    calculate_monthly_summary,
    category_expense_analysis
)

from app.db.redis import get_or_set_cache
from app.services.insight_service import generate_insights
from app.services.trend_service import get_monthly_trend


router = APIRouter(
    prefix="/insights",
    tags=["Insights"]
)

# -------------------------------------------------
# MONTHLY SUMMARY
# -------------------------------------------------

@router.get("/summary")
def get_monthly_summary(
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    year: int = Query(default=datetime.now().year),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns income, expense, and savings for a given month/year.
    """

    return calculate_monthly_summary(
        db=db,
        user_id=current_user.id,
        month=month,
        year=year
    )


# -------------------------------------------------
# CATEGORY-WISE ANALYSIS
# -------------------------------------------------

@router.get("/category")
def get_category_analysis(
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    year: int = Query(default=datetime.now().year),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns percentage-wise category expense distribution.
    """

    return category_expense_analysis(
        db=db,
        user_id=current_user.id,
        month=month,
        year=year
    )

@router.get("/recommendations")
def get_insights(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)  # ORM User
):
    user_id = user.id
    user_type = user.user_type

    cache_key = f"insights:{user_id}:{user_type}"

    return get_or_set_cache(
        cache_key,
        lambda: generate_insights(
            db=db,
            user_id=user_id,
            user_type=user_type
        ),
        expiry=600
    )



@router.get("/trend")
def monthly_trend(
    year: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_id = user.id

    # Structured cache key (production style)
    cache_key = f"analytics:trend:{user_id}:{year}"

    return get_or_set_cache(
        cache_key,
        lambda: get_monthly_trend(db, user_id, year),
        expiry=600  # 10 minutes cache
    )
