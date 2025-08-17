# backend/app/services/point_service.py

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ..models import points as points_model
from ..models.points import PointReason

# Define the value of different actions
POINT_VALUES = {
    PointReason.WASTE_UPLOAD_APPROVED: 10,
    PointReason.SIGNUP_BONUS: 50,
}


def add_points(db: Session, user_id: int, reason: PointReason, description: str, points_override: int = None):
    """
    Adds an entry to the points ledger. Can be positive (earning) or negative (spending).
    """
    if points_override is not None:
        points_change = points_override
    else:
        points_change = POINT_VALUES.get(reason, 0)

    ledger_entry = points_model.PointsLedger(
        user_id=user_id,
        points_change=points_change,
        reason=reason,
        description=description
    )
    db.add(ledger_entry)
    # The commit will be handled by the calling function or route dependency
    return ledger_entry


def get_user_point_balance(db: Session, user_id: int) -> int:
    """
    Calculates a user's total points by summing their ledger entries.
    """
    total_points = db.query(func.sum(points_model.PointsLedger.points_change)).filter(
        points_model.PointsLedger.user_id == user_id
    ).scalar()
    return total_points or 0


def get_user_point_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(points_model.PointsLedger).filter(
        points_model.PointsLedger.user_id == user_id
    ).order_by(points_model.PointsLedger.created_at.desc()).offset(skip).limit(limit).all()