# app/api/api_v1/endpoints/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.session import get_db
from app.db.model import User
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}
