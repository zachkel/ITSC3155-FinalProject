from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import reviews as review_schema
from ..models import reviews as review_model

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

@router.post("/", response_model=review_schema.Review)
def create_review(review: review_schema.ReviewCreate, db: Session = Depends(get_db)):
    db_review = review_model.Reviews(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/", response_model=list[review_schema.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = db.query(review_model.Reviews).offset(skip).limit(limit).all()
    return reviews


@router.put("/{review_id}", response_model=review_schema.Review)
def update_review(review_id: int, review: review_schema.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(review_model.Reviews).filter(review_model.Reviews.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    update_data = review.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/{review_id}", response_model=review_schema.Review)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(review_model.Reviews).filter(review_model.Reviews.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return db_review