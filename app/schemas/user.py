from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# what user sends to register
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

# what we send back (never send password!)
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# token response after login
class Token(BaseModel):
    access_token: str
    token_type: str

# data stored inside the token
class TokenData(BaseModel):
    email: Optional[str] = None
