from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    HOTEL_OWNER = "hotel_owner"

class AiJobStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobTriggerType(str, enum.Enum):
    MANUAL = "manual"
    BATCH = "batch"
    GUARDRAIL = "guardrail"

class QuestionStatus(str, enum.Enum):
    PENDING = "pending"
    ANSWERED = "answered"
    IGNORED = "ignored"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.HOTEL_OWNER)
    is_active = Column(Boolean, default=True)
    # Simplified auth for now, email/hashed_password would go here
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    hotels = relationship("Hotel", back_populates="owner")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    official_url = Column(String)
    booking_engine_url = Column(String)
    stripe_account_id = Column(String, nullable=True)

    owner = relationship("User", back_populates="hotels")
    contents = relationship("HotelContent", back_populates="hotel", uselist=False)
    unanswered_questions = relationship("UnansweredQuestion", back_populates="hotel")

class HotelContent(Base):
    __tablename__ = "hotel_contents"

    hotel_id = Column(Integer, ForeignKey("hotels.id"), primary_key=True)
    scraped_data = Column(JSON, default={})
    last_analyzed_at = Column(DateTime(timezone=True), nullable=True)
    image_assets = Column(JSON, default={})

    hotel = relationship("Hotel", back_populates="contents")

class AiScrapeJob(Base):
    __tablename__ = "ai_scrape_jobs"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id")) # Assuming jobs are linked to hotels, though not explicitly in spec, it makes sense.
    status = Column(Enum(AiJobStatus), default=AiJobStatus.QUEUED)
    trigger_type = Column(Enum(JobTriggerType), default=JobTriggerType.MANUAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    user_query = Column(Text)
    status = Column(Enum(QuestionStatus), default=QuestionStatus.PENDING)
    answer_text = Column(Text, nullable=True)
    notification_sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hotel = relationship("Hotel", back_populates="unanswered_questions")
