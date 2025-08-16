# backend/app/routes/points.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import user_schema, point_schema
from app.services import point_service
from app.database import get_db
from app.services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/points",
    tags=["Points & Rewards"]
)

# Note: For the response_model below, you should add a new Pydantic schema
# to `point_schema.py` like this for better validation:
#
# class PointBalance(BaseModel):
#     user_id: int
#     current_balance: int

@router.get("/my-balance", response_model=dict)
def get_my_point_balance(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Retrieves the current point balance for the authenticated user.
    """
    balance = point_service.get_user_point_balance(db, user_id=current_user.id)
    return {"user_id": current_user.id, "current_balance": balance}


@router.get("/my-history", response_model=List[point_schema.PointsLedger])
def get_my_point_history(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieves the transaction history for the authenticated user's points.
    """
    history = point_service.get_user_point_history(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return history