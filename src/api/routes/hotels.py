from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import database, models
from ...schemas import schemas
from ...crud import crud_hotel
from ...api import deps

router = APIRouter(prefix="/api/hotels", tags=["hotels"])

@router.post("/", response_model=schemas.Hotel)
def create_hotel(
    hotel: schemas.HotelCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new hotel.
    """
    return crud_hotel.create_hotel(db=db, hotel=hotel, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.Hotel])
def read_hotels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve hotels.
    If Super Admin, retrieve all hotels.
    If Hotel Owner, retrieve only owned hotels.
    """
    if current_user.role == models.UserRole.SUPER_ADMIN:
        hotels = crud_hotel.get_all_hotels(db, skip=skip, limit=limit)
    else:
        hotels = crud_hotel.get_hotels_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return hotels

@router.get("/{hotel_id}", response_model=schemas.Hotel)
def read_hotel(
    hotel_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get a specific hotel by ID.
    """
    hotel = crud_hotel.get_hotel(db, hotel_id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    if current_user.role != models.UserRole.SUPER_ADMIN and hotel.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return hotel

@router.put("/{hotel_id}", response_model=schemas.Hotel)
def update_hotel(
    hotel_id: int,
    hotel_in: schemas.HotelUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update a hotel.
    """
    hotel = crud_hotel.get_hotel(db, hotel_id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    if current_user.role != models.UserRole.SUPER_ADMIN and hotel.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    hotel = crud_hotel.update_hotel(db, db_hotel=hotel, hotel_update=hotel_in)
    return hotel
