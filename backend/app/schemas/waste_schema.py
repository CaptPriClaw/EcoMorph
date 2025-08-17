# backend/app/schemas/waste_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.waste import WasteStatus


class WasteBase(BaseModel):
    material_type: str
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    image_url: str


class WasteCreate(WasteBase):
    pass


class WasteUpdate(BaseModel):
    status: Optional[WasteStatus] = None


class Waste(WasteBase):
    id: int
    uploader_id: int
    status: WasteStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True