from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -------- المستخدم --------
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        from_attributes = True  # بدل orm_mode في Pydantic v2

# -------- التوكن --------
class Token(BaseModel):
    access_token: str
    token_type: str

# -------- المعاملات --------
class TransactionBase(BaseModel):
    amount: float
    type: str  # "charge" أو "payment"

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# -------- رصيد المستخدم --------
class BalanceOut(BaseModel):
    balance: float

    class Config:
        from_attributes = True

# -------- الشحن --------
class ChargeBalance(BaseModel):
    amount: float

# -------- الدفع --------
class PayAmount(BaseModel):
    amount: float
