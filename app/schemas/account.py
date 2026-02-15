from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AccountType(str, Enum):
    savings = "savings"
    checking = "checking"

class AccountCreate(BaseModel):
    account_type: AccountType = AccountType.savings

class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: AccountType
    balance: float
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
