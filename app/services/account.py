from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.account import Account
from app.schemas.account import AccountCreate
import random
import string

def generate_account_number() -> str:
    return ''.join(random.choices(string.digits, k=12))

async def create_account(db: AsyncSession, user_id: int, account_data: AccountCreate):
    # generate unique account number
    while True:
        account_number = generate_account_number()
        result = await db.execute(
            select(Account).where(Account.account_number == account_number)
        )
        if not result.scalar_one_or_none():
            break

    new_account = Account(
        account_number=account_number,
        account_type=account_data.account_type,
        balance=0.00,
        owner_id=user_id
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account

async def get_user_accounts(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Account).where(Account.owner_id == user_id)
    )
    return result.scalars().all()

async def get_account_by_id(db: AsyncSession, account_id: int):
    result = await db.execute(
        select(Account).where(Account.id == account_id)
    )
    return result.scalar_one_or_none()
