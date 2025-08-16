# backend/app/models/points.py

import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# from app.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PointReason(enum.Enum):
    WASTE_UPLOAD_APPROVED = "waste_upload_approved"
    PRODUCT_SALE = "product_sale"
    PRODUCT_PURCHASE = "product_purchase"
    ADMIN_ADJUSTMENT = "admin_adjustment"
    SIGNUP_BONUS = "signup_bonus"


class PointsLedger(Base):
    __tablename__ = "points_ledger"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    points_change = Column(Integer, nullable=False)  # Can be positive (earn) or negative (spend)
    reason = Column(Enum(PointReason), nullable=False)
    description = Column(String, nullable=True)  # e.g., "Purchase of 'Bottle Lamp'"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="points_ledger")