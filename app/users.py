from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app import utils  # الملف الجديد

router = APIRouter()

# تسجيل المستخدم الجديد
@router.post("/register", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="اسم المستخدم موجود بالفعل")
    
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# تسجيل الدخول
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="البيانات غير صحيحة")
    
    access_token = utils.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

