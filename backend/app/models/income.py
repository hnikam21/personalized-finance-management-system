from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(100), nullable=False)

    # Use Numeric for financial precision
    amount = Column(Numeric(10, 2), nullable=False)

    date = Column(Date, nullable=False)

    recurring = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # ORM relationship
    user = relationship("User", backref="incomes")
