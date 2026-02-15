from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Account, Transaction
from app.routes import auth, accounts, transactions

app = FastAPI(title="Bank Transaction System")

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Bank API is running 🚀"}
