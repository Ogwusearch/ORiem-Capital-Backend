from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_model import User
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.services import account_service

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=["Accounts"]
)


@router.post("/", response_model=AccountResponse)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return account_service.create_account(db, user_id=current_user.id, data=data)


@router.get("/", response_model=List[AccountResponse])
def get_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return account_service.get_user_accounts(db, user_id=current_user.id)
