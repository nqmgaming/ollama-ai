from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.token import Token

router = APIRouter()


@router.post("/generate_quiz")
def generate_quiz(topic: str, db: Session = Depends(get_db)):
    # Logic to generate quiz
    return {"message": "Quiz generated successfully"}
