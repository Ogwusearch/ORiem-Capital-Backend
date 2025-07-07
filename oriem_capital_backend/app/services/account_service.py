
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.account_model import Account
from app.schemas.account_schema import AccountCreate
from app.models.user_model import User
from datetime import datetime
import random

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def create_account(db: Session, data: AccountCreate, user: User):
    account = Account(
        owner_id=user.id,
        account_type=data.account_type,
        account_number=generate_account_number(),
        balance=0.0,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_user_accounts(db: Session, user: User):
    return db.query(Account).filter(Account.owner_id == user.id).all()

def get_account_by_id(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()

def toggle_account_freeze_status(db: Session, account_id: int, freeze: bool):
    account = get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.is_active = not freeze
    db.commit()
    db.refresh(account)
    return account
