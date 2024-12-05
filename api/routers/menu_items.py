from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import menu_items as models
from ..schemas import menu_items as schemas

router = APIRouter(
    tags=['Menu Items'],
    prefix="/menu_items"
)

@router.post('/menu-items/', response_model=schemas.MenuItem)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_item = models.MenuItems(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/menu-items/{item_id}', response_model=schemas.MenuItem)
def update_menu_item(item_id: int, item: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.MenuItems).filter(models.MenuItems.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Menu item not found')
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/menu-items/{item_id}', response_model=schemas.MenuItem)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.MenuItems).filter(models.MenuItems.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Menu item not found')
    db.delete(db_item)
    db.commit()
    return db_item