# backend/app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import user_schema
from app.services import user_service
from app.database import get_db
from app.services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Handles user registration.
    """
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # You could also add a signup bonus here via the point_service
    # point_service.add_points(db, user_id=new_user.id, reason=PointReason.SIGNUP_BONUS)

    return user_service.create_user(db=db, user=user)


@router.get("/me", response_model=user_schema.User)
def read_users_me(current_user: user_schema.User = Depends(get_current_active_user)):
    """
    Fetches the profile of the currently authenticated user.
    """
    return current_user


@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetches a user profile by their ID.
    (This might be an admin-only endpoint in a real application)
    """
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user