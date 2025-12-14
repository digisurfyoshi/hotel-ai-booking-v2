from fastapi import APIRouter
from src.api.v1.endpoints import users, hotels, questions, jobs

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(hotels.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
