from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from typing import Optional, Literal


# ----------- INPUT SCHEMAS -----------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)

    # Restrict allowed values
    user_type: Literal["dependent", "independent"]

    monthly_income: Optional[Decimal] = None
    risk_profile: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ----------- RESPONSE SCHEMAS -----------

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: str
    monthly_income: Optional[Decimal]
    risk_profile: Optional[str]

    class Config:
        from_attributes = True   # Pydantic v2 (orm_mode equivalent)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
