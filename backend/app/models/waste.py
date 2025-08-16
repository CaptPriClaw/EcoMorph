# backend/app/models/waste.py

import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# from app.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WasteStatus(enum.Enum):
    PENDING_VERIFICATION = "pending_verification"
    APPROVED = "approved"
    REJECTED = "rejected"
    UPCYCLED = "upcycled"


class Waste(Base):
    __tablename__ = "wastes"

    id = Column(Integer, primary_key=True, index=True)
    material_type = Column(String, index=True, nullable=False)
    description = Column(String)
    weight_kg = Column(Float, nullable=True)
    image_url = Column(String, nullable=False)
    status = Column(Enum(WasteStatus), nullable=False, default=WasteStatus.PENDING_VERIFICATION)

    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to User
    uploader = relationship("User", back_populates="wastes")