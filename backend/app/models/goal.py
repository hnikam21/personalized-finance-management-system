from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime,
    Numeric
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    # Financial precision
    target_amount = Column(Numeric(10, 2), nullable=False)
    saved_amount = Column(Numeric(10, 2), default=0, nullable=False)

    deadline = Column(Date, nullable=True)

    # Example: 1 = high, 2 = medium, 3 = low
    priority = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # ORM relationship
    user = relationship("User", backref="goals")
