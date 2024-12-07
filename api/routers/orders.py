from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import orders as models
from ..models import menu_items as menu_items_models
from ..models import order_details as order_details_models
from ..schemas import orders as schemas
from datetime import datetime

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post('/', response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    total_price = Decimal('0.00')
    db_order_detail = models.Orders(item_id = order.item_id, quantity=order.quantity)

    for item_id, quantity in order:
        menu_item = db.query(menu_items_models.MenuItems).filter(menu_items_models.MenuItems.id == item_id).first()
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f'Menu item with ID {item_id} not found')

        total_price += Decimal(str(menu_item.price)) * quantity

    db_order = models.Orders(
        customer_id=order.customer_id,
        tracking_number=order.tracking_number,
        order_status=order.order_status,
        total_price=total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_order_detail = models.OrderDetail(
            order_id=db_order.id,
            item_id=item.item_id,
            quantity=item.quantity
        )
        db.add(db_order_detail)

    db.commit()
    return db_order

@router.get('/', response_model=list[schemas.Order])
def read_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Orders).all()

@router.get('/revenue/{date}', response_model=float)
def get_revenue_by_date(date: datetime, db: Session = Depends(get_db)):
    revenue = db.query(func.sum(models.Orders.total_price)).filter(models.Orders.order_date == date).scalar()
    return revenue if revenue else 0.0

@router.get('/date-range', response_model=list[schemas.Order])
def read_orders_by_date_range(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    order = db.query(models.Orders).filter(models.Orders.order_date.between(start_date, end_date)).all()
    if not order:
        raise HTTPException(status_code=404, detail='No orders found within the specified date range')
    return order

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
def get_order_history(costumer_id: int = None, db: Session = Depends(get_db)):
    if costumer_id:
        orders = db.query(models.Orders).filter(models.Orders.costumer_id == costumer_id).all()
    else:
        orders = db.query(models.Orders).all()
    if not orders:
        raise HTTPException(status_code=404, detail='No orders found')
    return orders