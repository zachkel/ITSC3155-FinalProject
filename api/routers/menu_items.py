from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import menu_items as models
from ..schemas import menu_items as schemas

router = APIRouter(
    tags=['Menu Items'],
    prefix="/menu_items"
)

@router.post('/', response_model=schemas.MenuItem)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_menu_item = models.MenuItems(**item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.put('/{item_id}', response_model=schemas.MenuItem)
def update_menu_item(item_id: int, item: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.MenuItems).filter(models.MenuItems.id == item_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail='Menu item not found')
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_menu_item, key, value)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.delete('/{item_id}', response_model=schemas.MenuItem)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    db_menu_item = db.query(models.MenuItems).filter(models.MenuItems.id == item_id).first()
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail='Menu item not found')
    db.delete(db_menu_item)
    db.commit()
    return db_menu_item

@router.get('/search', response_model=list[schemas.MenuItem])
def search_menu_items(q: str, db: Session = Depends(get_db)):
    menu_items = db.query(models.MenuItems).filter(models.MenuItems.name.contains(q)).all()
    return menu_items