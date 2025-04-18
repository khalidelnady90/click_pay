from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database


router = APIRouter()

# إنشاء معاملة جديدة (شحن أو دفع)
@router.post("/transactions", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    new_transaction = models.Transaction(amount=transaction.amount, type=transaction.type, user_id=transaction.user_id)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
