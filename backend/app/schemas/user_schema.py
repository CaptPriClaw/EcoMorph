# backend/app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Import schemas that might be nested in a user response
from .waste_schema import Waste
from .product_schema import Product
from .points_schema import PointsLedger
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.UPLOADER


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# This is the main schema for reading/returning user data from the API
class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    # We will add these relationships after all schemas are defined
    # to avoid circular imports. For now, they are commented out.
    # wastes: List[Waste] = []
    # products: List[Product] = []
    # points_ledger: List[PointsLedger] = []

    class Config:
        orm_mode = True