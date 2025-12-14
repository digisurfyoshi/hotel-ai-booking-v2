from sqlalchemy.orm import Session
from src.db import models
from src.schemas import schemas
from typing import List, Optional

# --- User CRUD ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # In a real app, hash the password here
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, role=user.role, is_active=user.is_active)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# --- Hotel CRUD ---
def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_hotels_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).filter(models.Hotel.owner_id == owner_id).offset(skip).limit(limit).all()

def create_hotel(db: Session, hotel: schemas.HotelCreate, owner_id: int):
    db_hotel = models.Hotel(**hotel.dict(), owner_id=owner_id)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

# --- Question CRUD ---
def get_questions_by_hotel(db: Session, hotel_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.UnansweredQuestion).filter(models.UnansweredQuestion.hotel_id == hotel_id).offset(skip).limit(limit).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.UnansweredQuestion(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def update_question_answer(db: Session, question_id: int, answer_text: str):
    db_question = db.query(models.UnansweredQuestion).filter(models.UnansweredQuestion.id == question_id).first()
    if db_question:
        db_question.answer_text = answer_text
        db_question.status = models.QuestionStatus.ANSWERED
        db.commit()
        db.refresh(db_question)
    return db_question
