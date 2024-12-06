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


@router.get("/", response_model=list[payment_schema.Payment])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = db.query(payment_model.Payment).offset(skip).limit(limit).all()
    return payments


@router.put("/{payment_id}", response_model=payment_schema.Payment)
def update_payment(payment_id: int, payment: payment_schema.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(payment_model.Payment).filter(payment_model.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    update_data = payment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment


@router.delete("/{payment_id}", response_model=payment_schema.Payment)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(payment_model.Payment).filter(payment_model.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(db_payment)
    db.commit()
    return db_payment