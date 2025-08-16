# backend/app/services/waste_service.py

from sqlalchemy.orm import Session
from typing import Optional

from app.models import waste as waste_model
from app.schemas import waste_schema
from app.models.waste import WasteStatus

def create_waste(db: Session, waste: waste_schema.WasteCreate, uploader_id: int) -> waste_model.Waste:
    db_waste = waste_model.Waste(**waste.dict(), uploader_id=uploader_id)
    db.add(db_waste)
    db.commit()
    db.refresh(db_waste)
    return db_waste

def get_waste(db: Session, waste_id: int) -> Optional[waste_model.Waste]:
    return db.query(waste_model.Waste).filter(waste_model.Waste.id == waste_id).first()

def get_wastes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[waste_model.Waste]:
    return db.query(waste_model.Waste).filter(waste_model.Waste.uploader_id == user_id).offset(skip).limit(limit).all()

def update_waste_status(db: Session, waste_id: int, status: WasteStatus) -> Optional[waste_model.Waste]:
    db_waste = get_waste(db, waste_id=waste_id)
    if db_waste:
        db_waste.status = status
        db.commit()
        db.refresh(db_waste)
    return db_waste