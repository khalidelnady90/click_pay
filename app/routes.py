from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database, auth
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# تسجيل مستخدم جديد
@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="اسم المستخدم موجود بالفعل")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# تسجيل الدخول
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="فشل في تسجيل الدخول. تأكد من بياناتك")

    access_token = auth.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# استعلام عن الرصيد
@router.get("/balance", response_model=schemas.BalanceOut)
def get_balance(current_user: models.User = Depends(auth.get_current_user)):
    return {"balance": current_user.balance}

# شحن الرصيد
@router.post("/charge")
def charge_balance(charge: schemas.ChargeBalance, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.balance += charge.amount
    db.commit()
    return {"message": "تم شحن الرصيد بنجاح", "new_balance": current_user.balance}

# دفع مبلغ
@router.post("/pay")
def pay_amount(payment: schemas.PayAmount, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if current_user.balance < payment.amount:
        raise HTTPException(status_code=400, detail="الرصيد غير كافٍ")

    current_user.balance -= payment.amount
    transaction = models.Transaction(amount=payment.amount, user_id=current_user.id)
    db.add(transaction)
    db.commit()
    return {"message": "تم الدفع بنجاح", "remaining_balance": current_user.balance}

# سجل المعاملات
@router.get("/transactions", response_model=list[schemas.TransactionOut])
def get_transactions(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()
    return transactions
