# app/schemas/debt.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class DebtCreate(BaseModel):
    debt_type: str
    principal_amount: int
    interest_rate: Optional[float] = None
    due_date: Optional[date] = None


class DebtResponse(DebtCreate):
    id: int

    class Config:
        from_attributes = True
