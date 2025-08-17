# backend/app/services/product_service.py

from sqlalchemy.orm import Session
from typing import Optional

from ..models import product as product_model
from ..schemas import product_schema
from ..models.product import ProductStatus

def create_product(db: Session, product: product_schema.ProductCreate, upcycler_id: int) -> product_model.Product:
    db_product = product_model.Product(**product.dict(), upcycler_id=upcycler_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int) -> Optional[product_model.Product]:
    return db.query(product_model.Product).filter(product_model.Product.id == product_id).first()

def get_products_by_user(db: Session, user_id: int) -> list[product_model.Product]:
    return db.query(product_model.Product).filter(product_model.Product.upcycler_id == user_id).all()

def get_available_products(db: Session, skip: int = 0, limit: int = 100) -> list[product_model.Product]:
    return db.query(product_model.Product).filter(product_model.Product.status == ProductStatus.AVAILABLE).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_update: product_schema.ProductUpdate) -> Optional[product_model.Product]:
    db_product = get_product(db, product_id=product_id)
    if db_product:
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product