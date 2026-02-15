from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    DateTime,
    Numeric
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    # Financial precision
    amount = Column(Numeric(10, 2), nullable=False)

    date = Column(Date, nullable=False)

    description = Column(String(255), nullable=True)

    auto_categorized = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # ORM relationships
    user = relationship("User", backref="expenses")
    category = relationship("Category", backref="expenses")
