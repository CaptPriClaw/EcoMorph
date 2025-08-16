# backend/app/routes/marketplace.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import product_schema, user_schema, transaction_schema
from app.services import product_service, marketplace_service
from app.database import get_db
from app.services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/marketplace",
    tags=["Marketplace"]
)

@router.get("/", response_model=List[product_schema.Product])
def browse_available_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Public endpoint to browse all products currently available for sale.
    """
    products = product_service.get_available_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=product_schema.Product)
def view_product_details(product_id: int, db: Session = Depends(get_db)):
    """
    Public endpoint to view the details of a single product.
    """
    product = product_service.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/buy/{product_id}", response_model=transaction_schema.Transaction)
def buy_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user)
):
    """
    Allows an authenticated user to purchase a product using their points.
    This is a transactional endpoint.
    """
    product_to_buy = product_service.get_product(db, product_id=product_id)

    # 1. Validation checks
    if not product_to_buy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    if product_to_buy.status.value != "available":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is no longer available.")
    if product_to_buy.upcycler_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot buy your own product.")

    # 2. Execute the purchase via the service layer
    try:
        transaction = marketplace_service.execute_purchase(
            db=db,
            buyer=current_user,
            product=product_to_buy
        )
        return transaction
    except ValueError as e:
        # The service layer can raise a ValueError for business logic errors (e.g., insufficient points)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during the transaction.")