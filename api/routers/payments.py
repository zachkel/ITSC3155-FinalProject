from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import payment as payment_schema
from ..models import payment as payment_model

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)

@router.post("/", response_model=payment_schema.Payment)
def create_payment(payment: payment_schema.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = payment_model.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment