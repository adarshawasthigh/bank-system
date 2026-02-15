from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal

class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"

class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class DepositWithdrawRequest(BaseModel):
    account_id: int
    amount: Decimal
    description: Optional[str] = None

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    transaction_type: TransactionType
    status: TransactionStatus
    description: Optional[str]
    account_id: int
    created_at: datetime

    class Config:
        from_attributes = True
