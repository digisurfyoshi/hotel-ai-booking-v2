from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.crud import crud
from src.schemas import schemas
from src.api import deps
from src.db import models

router = APIRouter()

@router.get("/", response_model=List[schemas.Hotel])
def read_hotels(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # If user is admin, show all? If owner, show only theirs?
    # For simplicity now, show all if admin (or just all for MVP)
    # Ideally:
    # if current_user.role == models.UserRole.SUPER_ADMIN:
    #     return crud.get_hotels(db, skip=skip, limit=limit)
    # return crud.get_hotels_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return crud.get_hotels_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Hotel)
def create_hotel(
    hotel: schemas.HotelCreate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    return crud.create_hotel(db=db, hotel=hotel, owner_id=current_user.id)

@router.get("/{hotel_id}", response_model=schemas.Hotel)
def read_hotel(
    hotel_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    db_hotel = crud.get_hotel(db, hotel_id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    # Check permission
    if db_hotel.owner_id != current_user.id and current_user.role != models.UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db_hotel
