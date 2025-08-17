# backend/app/services/user_service.py

from sqlalchemy.orm import Session
from typing import Optional

# --- CHANGED ---
from ..models import user as user_model
from ..schemas import user_schema
from . import auth_service # Changed to relative
# ---------------

def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = auth_service.get_password_hash(user.password)
    db_user = user_model.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user