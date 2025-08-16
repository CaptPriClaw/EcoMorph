# backend/app/schemas/waste_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.waste import WasteStatus

# Forward declaration for nested user schema
from .user_schema import User


class WasteBase(BaseModel):
    material_type: str
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    image_url: str


class WasteCreate(WasteBase):
    pass


class WasteUpdate(BaseModel):
    material_type: Optional[str] = None
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    status: Optional[WasteStatus] = None


class Waste(WasteBase):
    id: int
    uploader_id: int
    status: WasteStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Nested schema to include uploader's info when reading waste data
    # uploader: User # This will cause circular import issues if not handled carefully

    class Config:
        orm_mode = True  # Allows Pydantic to map to ORM objects