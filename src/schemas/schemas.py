from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# --- Enums (Matching models.py) ---
class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    HOTEL_OWNER = "hotel_owner"

class AiJobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobTriggerType(str, Enum):
    MANUAL = "manual"
    BATCH = "batch"
    GUARDRAIL = "guardrail"

class QuestionStatus(str, Enum):
    PENDING = "pending"
    ANSWERED = "answered"
    IGNORED = "ignored"

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.HOTEL_OWNER
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

# --- Hotel Schemas ---
class HotelBase(BaseModel):
    name: str
    official_url: Optional[str] = None
    booking_engine_url: Optional[str] = None
    stripe_account_id: Optional[str] = None

class HotelCreate(HotelBase):
    pass # owner_id will be assigned via current_user or admin

class HotelUpdate(HotelBase):
    name: Optional[str] = None

class Hotel(HotelBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True

# --- Question Schemas ---
class QuestionBase(BaseModel):
    user_query: str
    status: QuestionStatus = QuestionStatus.PENDING
    answer_text: Optional[str] = None

class QuestionCreate(BaseModel):
    user_query: str
    hotel_id: int # Depending on implementation, might not need this if creating under a hotel context
    
class QuestionUpdate(BaseModel):
    status: Optional[QuestionStatus] = None
    answer_text: Optional[str] = None

class Question(QuestionBase):
    id: int
    hotel_id: int
    created_at: datetime
    notification_sent_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# --- Scrape Job Schemas ---
class ScrapeJobBase(BaseModel):
    trigger_type: JobTriggerType = JobTriggerType.MANUAL

class ScrapeJobCreate(ScrapeJobBase):
    hotel_id: int

class ScrapeJob(ScrapeJobBase):
    id: int
    hotel_id: int
    status: AiJobStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
