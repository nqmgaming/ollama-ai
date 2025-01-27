from fastapi import APIRouter
from app.api.api_v1.endpoints import login, quiz, user

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(quiz.router, prefix="/quizzes", tags=["quizzes"])
