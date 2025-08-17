# backend/app/services/marketplace_service.py

from sqlalchemy.orm import Session

# --- CHANGED ---
from ..models import user as user_model
from ..models import product as product_model
from ..models import transaction as transaction_model
from ..models.product import ProductStatus
from ..models.points import PointReason
from . import point_service
# ---------------

def execute_purchase(
    db: Session,
    buyer: user_model.User,
    product: product_model.Product
):
    # ... (rest of the file is unchanged) ...
    buyer_balance = point_service.get_user_point_balance(db, user_id=buyer.id)
    if buyer_balance < product.price_points:
        raise ValueError("Insufficient points to complete the purchase.")

    db_transaction = transaction_model.Transaction(
        product_id=product.id,
        buyer_id=buyer.id,
        seller_id=product.upcycler_id,
        points_exchanged=product.price_points
    )
    db.add(db_transaction)
    product.status = ProductStatus.SOLD

    point_service.add_points(
        db, user_id=buyer.id, reason=PointReason.PRODUCT_PURCHASE,
        description=f"Purchase of '{product.name}'", points_override=-product.price_points
    )
    point_service.add_points(
        db, user_id=product.upcycler_id, reason=PointReason.PRODUCT_SALE,
        description=f"Sale of '{product.name}'", points_override=product.price_points
    )

    db.commit()
    db.refresh(db_transaction)
    return db_transaction