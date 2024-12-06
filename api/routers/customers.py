from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import customer as customer_schema
from ..models import customer as customer_model

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

@router.post("/", response_model=customer_schema.Customer)
def create_customer(customer: customer_schema.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = customer_model.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer