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


@router.put("/{promotion_id}", response_model=promotion_schema.Promotion)
def update_promotion(promotion_id: int, promotion: promotion_schema.PromotionUpdate, db: Session = Depends(get_db)):
    db_promotion = db.query(promotion_model.Promotion).filter(promotion_model.Promotion.id == promotion_id).first()
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    update_data = promotion.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_promotion, key, value)

    db.commit()
    db.refresh(db_promotion)
    return db_promotion


@router.delete("/{promotion_id}", response_model=promotion_schema.Promotion)
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    db_promotion = db.query(promotion_model.Promotion).filter(promotion_model.Promotion.id == promotion_id).first()
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    db.delete(db_promotion)
    db.commit()
    return db_promotion