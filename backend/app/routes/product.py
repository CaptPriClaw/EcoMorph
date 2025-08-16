# backend/app/routes/product.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import product_schema, user_schema
from app.services import product_service
from app.database import get_db
from app.services.auth_service import get_current_active_user
from app.models.user import UserRole

router = APIRouter(
    prefix="/products",
    tags=["My Products (Upcycler)"]
)


@router.post("/", response_model=product_schema.Product, status_code=status.HTTP_201_CREATED)
def create_product_listing(
        product: product_schema.ProductCreate,
        db: Session = Depends(get_db),
        current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Creates a new product listing for the logged-in upcycler.
    """
    # Ensure the user has the 'upcycler' role
    if current_user.role != UserRole.UPCYCLER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users with the 'upcycler' role can create products."
        )
    return product_service.create_product(db=db, product=product, upcycler_id=current_user.id)


@router.get("/my-listings", response_model=List[product_schema.Product])
def read_my_product_listings(
        db: Session = Depends(get_db),
        current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Retrieves all product listings for the currently authenticated user.
    """
    return product_service.get_products_by_user(db=db, user_id=current_user.id)


@router.put("/{product_id}", response_model=product_schema.Product)
def update_my_product_listing(
        product_id: int,
        product_update: product_schema.ProductUpdate,
        db: Session = Depends(get_db),
        current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Updates a product listing. Ensures the user owns the product.
    """
    product = product_service.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.upcycler_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")

    return product_service.update_product(db=db, product_id=product_id, product_update=product_update)