from pydantic import BaseModel, Field, model_validator
from typing import Optional
from decimal import Decimal
from datetime import date


class InvestmentCreate(BaseModel):
    investment_type: str

    # Common
    start_date: Optional[date] = None
    auto_update: bool = True

    # FD / SIP
    principal_amount: Optional[Decimal] = None
    rate_of_return: Optional[Decimal] = None

    # STOCK
    quantity: Optional[Decimal] = None
    buy_price: Optional[Decimal] = None

    @model_validator(mode="after")
    def validate_fields(self):

        if self.investment_type in ["FD", "SIP"]:
            if not self.principal_amount:
                raise ValueError("principal_amount required for FD/SIP")

        if self.investment_type == "STOCK":
            if not self.quantity or not self.buy_price:
                raise ValueError("quantity and buy_price required for STOCK")

        return self


class InvestmentResponse(BaseModel):
    id: int
    investment_type: str
    principal_amount: Decimal
    current_value: Decimal
    rate_of_return: Optional[Decimal]
    compounding_frequency: Optional[str]
    symbol: Optional[str]
    quantity: Optional[Decimal]
    buy_price: Optional[Decimal]
    start_date: Optional[date]

    class Config:
        from_attributes = True


class SellInvestmentRequest(BaseModel):
    sell_price: Decimal
