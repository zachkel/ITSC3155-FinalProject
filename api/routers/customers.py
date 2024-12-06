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


@router.get("/", response_model=list[customer_schema.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(customer_model.Customer).offset(skip).limit(limit).all()
    return customers


@router.put("/{customer_id}", response_model=customer_schema.Customer)
def update_customer(customer_id: int, customer: customer_schema.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(customer_model.Customer).filter(customer_model.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.delete("/{customer_id}", response_model=customer_schema.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(customer_model.Customer).filter(customer_model.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()
    return db_customer