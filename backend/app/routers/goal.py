from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalResponse
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.user import User
from app.services.goal_allocation_service import allocate_monthly_savings

router = APIRouter(
    prefix="/goal",
    tags=["Goal"]
)

# ---------------- CREATE GOAL ----------------

@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED
)
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_goal = Goal(
        user_id=current_user.id,
        name=goal.name,
        target_amount=goal.target_amount,
        saved_amount=0,
        deadline=goal.deadline,
        priority=goal.priority
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


# ---------------- GOAL PROGRESS ----------------

@router.get("/progress")
def goal_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).all()

    result = []
    for g in goals:
        progress = (
            (g.saved_amount / g.target_amount) * 100
            if g.target_amount else 0
        )
        result.append({
            "goal": g.name,
            "progress": round(float(progress), 2)
        })

    return result

@router.post("/allocate-monthly")
def allocate_monthly(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return allocate_monthly_savings(db, user.id)

