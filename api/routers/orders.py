from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import orders as models
from ..models import menu_items as menu_items_models
from ..models import order_details as order_details_models
from ..models import resources as resources_models
from ..schemas import orders as schemas
from datetime import datetime

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post('/', response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    for item in order.items:
        menu_item = db.query(menu_items_models.MenuItems).filter(menu_items_models.MenuItems.id == item.item_id).first()
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f'Menu item with ID {item.item_id} not found')

        for ingredient in menu_item.ingredients:
            if ingredient.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f'Insufficient stock for ingredient {ingredient.name}')

    db_order = models.Orders(**order.dict(exclude={'items'}))
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_order_details = order_details_models.OrderDetail(order_id=db_order.id, menu_item_id=item.item_id, quantity=item.quantity)
        db.add(db_order_details)

        menu_item = db.query(menu_items_models.MenuItems).filter(menu_items_models.MenuItems.id == item.item_id).first()
        for ingredient in menu_item.ingredients:
            ingredient.stock -= item.quantity
            db.add(ingredient)

    db.commit()
    return db_order

@router.get('/', response_model=list[schemas.Order])
def read_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Orders).all()

@router.get('/revenue/{date}', response_model=float)
def get_revenue_by_date(date: datetime, db: Session = Depends(get_db)):
    revenue = db.query(func.sum(models.Orders.price)).filter(models.Orders.order_date == date).scalar()
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
def get_order_history(user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        orders = db.query(models.Orders).filter(models.Orders.user_id == user_id).all()
    else:
        orders = db.query(models.Orders).all()
    if not orders:
        raise HTTPException(status_code=404, detail='No orders found')
    return orders