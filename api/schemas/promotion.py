from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import DECIMAL


class PromotionBase(BaseModel):
    code: str
    discount_percent: Decimal
    start_date: datetime
    end_date: datetime

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    end_date: Optional[datetime] = None

class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True
