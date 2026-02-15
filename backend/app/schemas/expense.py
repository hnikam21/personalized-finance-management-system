from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date
from typing import Optional


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    category_id: Optional[int] = None 
    date: date
    description: Optional[str] = None


class ExpenseResponse(ExpenseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
