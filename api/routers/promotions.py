from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import promotion as promotion_schema
from ..models import promotion as promotion_model

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"],
)

@router.post("/", response_model=promotion_schema.Promotion)
def create_promotion(promotion: promotion_schema.PromotionCreate, db: Session = Depends(get_db)):
    db_promotion = promotion_model.Promotion(**promotion.dict())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

@router.get("/", response_model=list[promotion_schema.Promotion])
def read_promotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    promotions = db.query(promotion_model.Promotion).offset(skip).limit(limit).all()
    return promotions