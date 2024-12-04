from typing import Optional
from pydantic import BaseModel

class ReviewBase(BaseModel):
    review_text: Optional[str] = None
    score: int
    customer_id: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[int] = None

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True
