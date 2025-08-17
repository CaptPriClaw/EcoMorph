# backend/app/schemas/point_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.points import PointReason

class PointsLedgerBase(BaseModel):
    points_change: int
    reason: PointReason
    description: Optional[str] = None

class PointsLedgerCreate(PointsLedgerBase):
    user_id: int

class PointsLedger(PointsLedgerBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True