from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.crud import crud
from src.schemas import schemas
from src.api import deps
from src.db import models

router = APIRouter()

@router.get("/{hotel_id}/all", response_model=List[schemas.Question])
def read_questions(
    hotel_id: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # Verify hotel ownership or admin
    db_hotel = crud.get_hotel(db, hotel_id=hotel_id)
    if not db_hotel:
         raise HTTPException(status_code=404, detail="Hotel not found")
         
    if db_hotel.owner_id != current_user.id and current_user.role != models.UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return crud.get_questions_by_hotel(db, hotel_id=hotel_id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Question)
def create_question(
    question: schemas.QuestionCreate, 
    db: Session = Depends(deps.get_db)
):
    # Public endpoint? Or auth required? Assuming public for "ask query" from UI widget
    # But usually this comes from the AI system.
    # For now, let's assume it's created possibly without auth or via separate API key.
    # Allowing auth for testing.
    return crud.create_question(db=db, question=question)

@router.put("/{question_id}/answer", response_model=schemas.Question)
def answer_question(
    question_id: int,
    answer_text: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # Retrieve question to check hotel ownership
    # This logic should ideally be in CRUD or Service layer to allow efficiently checking perm
    pass # TODO: Add ownership check
    db_question = crud.update_question_answer(db, question_id=question_id, answer_text=answer_text)
    if not db_question:
         raise HTTPException(status_code=404, detail="Question not found")
    return db_question
