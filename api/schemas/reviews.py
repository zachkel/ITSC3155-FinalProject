from typing import Optional
from pydantic import BaseModel

class ReviewBase(BaseModel):
    comment: Optional[str] = None
    rating: int
    customer_id: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    comment: Optional[str] = None
    rating: Optional[int] = None

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True
