from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date
from typing import Optional


class GoalCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    target_amount: Decimal = Field(..., gt=0)
    deadline: date
    priority: int = Field(..., ge=1, le=5)


class GoalResponse(GoalCreate):
    id: int
    saved_amount: Decimal = Decimal("0")

    model_config = ConfigDict(from_attributes=True)
