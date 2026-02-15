from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvestmentCreate(BaseModel):
    investment_type: str
    amount: int
    expected_return: Optional[float] = None
    start_date: Optional[date] = None


class InvestmentResponse(InvestmentCreate):
    id: int

    class Config:
        from_attributes = True
