from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class GoalAllocation(Base):
    __tablename__ = "goal_allocations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    allocated_amount = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
