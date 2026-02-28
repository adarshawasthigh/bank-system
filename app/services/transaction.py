from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.transaction import Transaction, TransactionType, TransactionStatus
from app.models.account import Account
from app.schemas.transaction import DepositWithdrawRequest, TransferRequest
from decimal import Decimal

async def deposit(db: AsyncSession, data: DepositWithdrawRequest, user_id: int):
    result = await db.execute(select(Account).where(Account.id == data.account_id))
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not your account")
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    account.balance = Decimal(str(account.balance)) + data.amount

    txn = Transaction(
        amount=data.amount,
        transaction_type=TransactionType.deposit,
        status=TransactionStatus.completed,
        description=data.description,
        account_id=account.id
    )
    db.add(txn)
    await db.commit()
    await db.refresh(txn)
    return txn

async def withdraw(db: AsyncSession, data: DepositWithdrawRequest, user_id: int):
    result = await db.execute(select(Account).where(Account.id == data.account_id).with_for_update())
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not your account")
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    if Decimal(str(account.balance)) < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account.balance = Decimal(str(account.balance)) - data.amount

    txn = Transaction(
        amount=data.amount,
        transaction_type=TransactionType.withdrawal,
        status=TransactionStatus.completed,
        description=data.description,
        account_id=account.id
    )
    db.add(txn)
    await db.commit()
    await db.refresh(txn)
    return txn

async def transfer(db: AsyncSession, data: TransferRequest, user_id: int):
    from_result = await db.execute(select(Account).where(Account.id == data.from_account_id))
    from_account = from_result.scalar_one_or_none()

    to_result = await db.execute(select(Account).where(Account.id == data.to_account_id))
    to_account = to_result.scalar_one_or_none()

    if not from_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    if not to_account:
        raise HTTPException(status_code=404, detail="Destination account not found")
    if from_account.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not your account")
    if from_account.id == to_account.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    if Decimal(str(from_account.balance)) < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    from_account.balance = Decimal(str(from_account.balance)) - data.amount
    to_account.balance = Decimal(str(to_account.balance)) + data.amount

    debit_txn = Transaction(
        amount=data.amount,
        transaction_type=TransactionType.transfer,
        status=TransactionStatus.completed,
        description=f"Transfer to account {to_account.account_number}",
        account_id=from_account.id
    )
    credit_txn = Transaction(
        amount=data.amount,
        transaction_type=TransactionType.transfer,
        status=TransactionStatus.completed,
        description=f"Transfer from account {from_account.account_number}",
        account_id=to_account.id
    )
    db.add(debit_txn)
    db.add(credit_txn)
    await db.commit()
    await db.refresh(debit_txn)
    return debit_txn

async def get_transaction_history(db: AsyncSession, account_id: int, user_id: int):
    acc_result = await db.execute(select(Account).where(Account.id == account_id))
    account = acc_result.scalar_one_or_none()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not your account")

    result = await db.execute(
        select(Transaction)
        .where(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.desc())
    )
    return result.scalars().all()
