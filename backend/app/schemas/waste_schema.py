# backend/app/schemas/waste_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- CHANGED ---
from ..models.waste import WasteStatus


# ---------------

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

    class Config:
        orm_mode = True