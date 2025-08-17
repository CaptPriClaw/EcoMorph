# backend/app/models/product.py

import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# from ..database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductStatus(enum.Enum):
    AVAILABLE = "available"
    SOLD = "sold"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    image_url = Column(String, nullable=False)
    price_points = Column(Integer, nullable=False)  # Price in EcoPoints
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.AVAILABLE)

    upcycler_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to User
    upcycler = relationship("User", back_populates="products")

    # Relationship to Transactions
    transactions = relationship("Transaction", back_populates="product")