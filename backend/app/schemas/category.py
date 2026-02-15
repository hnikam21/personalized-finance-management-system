from pydantic import BaseModel, Field
from pydantic import ConfigDict
from decimal import Decimal
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    budget_limit: Optional[Decimal] = None


class CategoryResponse(CategoryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
