from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.api import deps
from src.db import models

router = APIRouter()

@router.post("/", response_model=schemas.ScrapeJob)
def create_scrape_job(
    job: schemas.ScrapeJobCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # Stub implementation
    # In reality, this would enqueue a background task (Celery, redis-queue, or Cloud Tasks)
    from datetime import datetime
    
    # Just return a mock response for now as we don't have job CRUD yet
    return schemas.ScrapeJob(
        id=1,
        hotel_id=job.hotel_id,
        trigger_type=job.trigger_type,
        status=models.AiJobStatus.QUEUED,
        created_at=datetime.now()
    )
