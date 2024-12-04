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

class OrderBase(BaseModel):
    customer_id: int
    tracking_number: str | None = None
    order_status: OrderStatus
    total_price: Decimal | None = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_status: OrderStatus


class Order(OrderBase):
    order_id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
