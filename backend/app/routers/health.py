from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.db.redis import get_or_set_cache
from app.services.health_score_service import calculate_health_score

router = APIRouter(prefix="/health", tags=["Health Score"])

@router.get("/score")
def get_health_score(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)  # user is ORM User now
):
    user_id = user.id
    user_type = user.user_type

    cache_key = f"health:{user_id}:{user_type}"

    return get_or_set_cache(
        cache_key,
        lambda: {
            "score": calculate_health_score(
                db=db,
                user_id=user_id,
                user_type=user_type
            )
        },
        expiry=600
    )



