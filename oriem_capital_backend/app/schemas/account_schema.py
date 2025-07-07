from pydantic import BaseModel, Field, validator
from enum import Enum


class AccountType(str, Enum):
    savings = "savings"
    checking = "checking"
    fixed_deposit = "fixed_deposit"
    investment = "investment"
    foreign_currency = "foreign_currency"
    escrow = "escrow"
    merchant = "merchant"
    offshore = "offshore"
    salary = "salary"


class AccountCreate(BaseModel):
    account_type: AccountType
    currency: str = Field(..., min_length=3, max_length=3)

    @validator("currency")
    def validate_currency(cls, v):
        if not v.isalpha() or len(v) != 3:
            raise ValueError("Currency must be a 3-letter alphabetic code.")
        return v.upper()


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: AccountType
    balance: float
    currency: str
    is_active: int

    class Config:
        orm_mode = True
