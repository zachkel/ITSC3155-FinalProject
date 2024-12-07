from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    in_route = "in-route"
    cancelled = "cancelled"

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_id: int
    tracking_number: str | None = None
    order_status: OrderStatus
    items: list[OrderItemCreate]

class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_status: OrderStatus


class Order(OrderBase):
    order_id: int
    total_price: Decimal
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = []

    class ConfigDict:
        from_attributes = True
