from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import orders as models
from ..schemas import orders as schemas
router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post('/', response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Orders(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get('/', response_model=list[schemas.Order])
def read_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Orders).all()


@router.get('/{order_id}', response_model=schemas.Order)
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail='Order not found')
    return db_order


@router.put('/{order_id}', response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail='Order not found')
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.delete('/{order_id}', response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail='Order not found')
    db.delete(db_order)
    db.commit()
    return db_order


@router.get("/history/", response_model=list[schemas.Order])
def get_order_history(user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        orders = db.query(models.Orders).filter(models.Orders.user_id == user_id).all()
    else:
        orders = db.query(models.Orders).all()
    if not orders:
        raise HTTPException(status_code=404, detail='No orders found')
    return orders