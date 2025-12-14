from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import models
from src.crud import crud
from src.schemas import schemas

# Dependency to get DB session is already imported as get_db

# Mock Dependency for Auth (Replace with OAuth2 in production)
def get_current_user(db: Session = Depends(get_db)):
    # This is a stub! In a real app, parse the token and get the user.
    # For now, we return the first user or create a super admin if none exists.
    user = crud.get_user(db, user_id=1)
    if not user:
        # Create a default super admin for testing purposes immediately if not distinct from seed data
        user_in = schemas.UserCreate(
            email="admin@example.com", 
            password="admin", 
            role=models.UserRole.SUPER_ADMIN
        )
        user = crud.create_user(db, user=user_in)
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
