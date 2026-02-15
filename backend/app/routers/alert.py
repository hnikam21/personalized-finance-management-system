from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db
from app.utils.auth_dependencies import get_current_user
from app.models.alert import Alert
from app.services.alert_service import generate_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/generate")
def trigger_alerts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)  # ORM User
):
    generate_alerts(db, user.id)
    return {"message": "Alerts generated"}


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)  # ORM User
):
    return db.query(Alert).filter(
        Alert.user_id == user.id
    ).order_by(Alert.created_at.desc()).all()
