from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    HOTEL_OWNER = "hotel_owner"

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.HOTEL_OWNER) # Storing as string for simplicity in SQLite/Postgres compatibility
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    hotels = relationship("Hotel", back_populates="owner")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    address = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="hotels")
    contents = relationship("HotelContent", back_populates="hotel")
    unanswered_questions = relationship("UnansweredQuestion", back_populates="hotel")
    scrape_jobs = relationship("AIScrapeJob", back_populates="hotel")

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    question_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hotel = relationship("Hotel", back_populates="unanswered_questions")

class HotelContent(Base):
    __tablename__ = "hotel_contents"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    content_type = Column(String, index=True) # e.g., 'faq', 'amenity', 'policy'
    content_data = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hotel = relationship("Hotel", back_populates="contents")

class AIScrapeJob(Base):
    __tablename__ = "ai_scrape_jobs"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    status = Column(String, default=JobStatus.PENDING)
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hotel = relationship("Hotel", back_populates="scrape_jobs")
