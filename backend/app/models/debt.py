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

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    debt_type = Column(String(50), nullable=False)

    # Financial precision
    principal_amount = Column(Numeric(10, 2), nullable=False)

    # Annual interest rate percentage (e.g. 12.50%)
    interest_rate = Column(Numeric(5, 2), nullable=True)

    due_date = Column(Date, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # ORM relationship
    user = relationship("User", backref="debts")
