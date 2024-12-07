from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class OrderDetailBase(BaseModel):
    order_id: int
    item_id: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None

class OrderDetail(OrderDetailBase):
    order_detail_id: int

    class ConfigDict:
        from_attributes = True