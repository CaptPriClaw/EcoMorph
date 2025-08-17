# backend/app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- CHANGED ---
from ..models.user import UserRole


# The other imports for Waste and Product schemas are already relative, which is good.
# We will handle the circular dependency later.
# from .waste_schema import Waste
# from .product_schema import Product
# ---------------

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.UPLOADER


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True