from sqlalchemy.orm import Session
from ..db import models
from ..schemas import schemas

def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_hotels_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).filter(models.Hotel.owner_id == owner_id).offset(skip).limit(limit).all()

def get_all_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).offset(skip).limit(limit).all()

def create_hotel(db: Session, hotel: schemas.HotelCreate, owner_id: int):
    db_hotel = models.Hotel(**hotel.dict(), owner_id=owner_id)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def update_hotel(db: Session, db_hotel: models.Hotel, hotel_update: schemas.HotelUpdate):
    update_data = hotel_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hotel, key, value)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def delete_hotel(db: Session, hotel_id: int):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if db_hotel:
        db.delete(db_hotel)
        db.commit()
    return db_hotel
