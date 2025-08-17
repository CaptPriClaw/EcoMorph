# backend/app/models/user.py

import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# It's assumed that a declarative base is created in your database.py file.
# from ..database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(enum.Enum):
    UPLOADER = "uploader"
    UPCYCLER = "upcycler"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.UPLOADER)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    wastes = relationship("Waste", back_populates="uploader")
    products = relationship("Product", back_populates="upcycler")
    points_ledger = relationship("PointsLedger", back_populates="user")

    # Relationships for transactions
    purchases = relationship("Transaction", foreign_keys="[Transaction.buyer_id]", back_populates="buyer")
    sales = relationship("Transaction", foreign_keys="[Transaction.seller_id]", back_populates="seller")