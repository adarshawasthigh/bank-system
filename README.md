# 🏦 Bank Transaction System API

A secure REST API for managing bank accounts and transactions, built with FastAPI and SQLAlchemy.

## 🚀 Features

- JWT Authentication (Register, Login, Protected Routes)
- Create & manage bank accounts (savings/checking)
- Deposit, Withdraw, and Transfer money between accounts
- Full transaction history per account
- Atomic transactions — money never lost or duplicated
- Auto-generated interactive API docs

## 🛠️ Tech Stack

- **FastAPI** — Modern Python web framework
- **SQLAlchemy** — Async ORM
- **SQLite** — Database (easily swappable to PostgreSQL/MySQL)
- **JWT (python-jose)** — Authentication tokens
- **Passlib + Bcrypt** — Password hashing
- **Pydantic** — Data validation

## 📁 Project Structure
```
bank_system/
├── app/
│   ├── main.py              # App entry point
│   ├── database.py          # DB connection
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── account.py
│   │   └── transaction.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── account.py
│   │   └── transaction.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── accounts.py
│   │   └── transactions.py
│   └── services/            # Business logic
│       ├── auth.py
│       ├── user.py
│       ├── account.py
│       └── transaction.py
├── .env.example
├── requirements.txt
└── README.md
```

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/bank-system.git
cd bank-system
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```bash
cp .env.example .env
```
Edit `.env` with your values.

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for interactive API docs.

## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user info |

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/` | Create bank account |
| GET | `/accounts/me` | Get all your accounts |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/deposit` | Deposit money |
| POST | `/transactions/withdraw` | Withdraw money |
| POST | `/transactions/transfer` | Transfer between accounts |
| GET | `/transactions/history/{account_id}` | Transaction history |

## 🔐 Authentication

All account and transaction endpoints require a Bearer token.

1. Register at `POST /auth/register`
2. Login at `POST /auth/login` to get your token
3. Click **Authorize** in `/docs` and paste your token

## 📄 Environment Variables

Create a `.env` file based on `.env.example`:
```env
DATABASE_URL=sqlite+aiosqlite:///./bankdb.sqlite3
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 👤 Author

**Adarsh Awasthi**  
GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
