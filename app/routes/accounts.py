from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.account import AccountCreate, AccountResponse
from app.services.account import create_account, get_user_accounts
from app.routes.auth import oauth2_scheme
from app.services.auth import verify_token
from app.services.user import get_user_by_email
from typing import List

router = APIRouter(prefix="/accounts", tags=["Accounts"])

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await get_user_by_email(db, token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=AccountResponse, status_code=201)
async def create_new_account(
    account_data: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await create_account(db, current_user.id, account_data)

@router.get("/me", response_model=List[AccountResponse])
async def get_my_accounts(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await get_user_accounts(db, current_user.id)
