# backend/app/schemas/product_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.product import ProductStatus


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: str
    price_points: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price_points: Optional[int] = None
    status: Optional[ProductStatus] = None


class Product(ProductBase):
    id: int
    upcycler_id: int
    status: ProductStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True