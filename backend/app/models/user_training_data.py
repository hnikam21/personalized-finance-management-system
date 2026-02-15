from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class UserTrainingData(Base):
    __tablename__ = "user_training_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String(255), nullable=False)
    category_name = Column(String(100), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
