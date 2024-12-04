from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    card_info: str
    transaction_status: str
    payment_type: str
    customer_id: int

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None

class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True
