from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.transaction import DepositWithdrawRequest, TransferRequest, TransactionResponse
from app.services.transaction import deposit, withdraw, transfer, get_transaction_history
from app.routes.auth import oauth2_scheme
from app.services.auth import verify_token
from app.services.user import get_user_by_email
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await get_user_by_email(db, token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/deposit", response_model=TransactionResponse)
async def make_deposit(
    data: DepositWithdrawRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await deposit(db, data, current_user.id)

@router.post("/withdraw", response_model=TransactionResponse)
async def make_withdrawal(
    data: DepositWithdrawRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await withdraw(db, data, current_user.id)

@router.post("/transfer", response_model=TransactionResponse)
async def make_transfer(
    data: TransferRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await transfer(db, data, current_user.id)

@router.get("/history/{account_id}", response_model=List[TransactionResponse])
async def transaction_history(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await get_transaction_history(db, account_id, current_user.id)
