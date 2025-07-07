from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AccountType(str, enum.Enum):
    savings = "savings"
    checking = "checking"  # Transactional account (aka current)
    fixed_deposit = "fixed_deposit"
    investment = "investment"
    foreign_currency = "foreign_currency"
    escrow = "escrow"
    merchant = "merchant"
    offshore = "offshore"
    salary = "salary"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    account_number = Column(String, unique=True, index=True, nullable=False)
    account_type = Column(Enum(AccountType), default=AccountType.savings, nullable=False)

    currency = Column(String(3), default="NGN")  # ISO 4217 e.g. USD, NGN, EUR
    balance = Column(Float, default=0.0)

    is_active = Column(Integer, default=1)  # 1 for active, 0 for frozen
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="accounts")
