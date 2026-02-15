from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class AlertSeverity(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    alert_type = Column(String(50), nullable=False)
    message = Column(String(255), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
