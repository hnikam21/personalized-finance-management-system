from pydantic import BaseModel, Field
from pydantic import ConfigDict
from decimal import Decimal
from datetime import date


class IncomeCreate(BaseModel):
    source: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., gt=0)
    date: date
    recurring: bool = False


class IncomeResponse(IncomeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
