# backend/app/services/marketplace_service.py

from sqlalchemy.orm import Session

from app.models import user as user_model
from app.models import product as product_model
from app.models import transaction as transaction_model
from app.models.product import ProductStatus
from app.models.points import PointReason
from app.services import point_service


def execute_purchase(
        db: Session,
        buyer: user_model.User,
        product: product_model.Product
) -> transaction_model.Transaction:
    """
    Executes the full logic for a product purchase.
    This function assumes initial checks (e.g., product availability) have been done.
    """
    # 1. Check if buyer has enough points
    buyer_balance = point_service.get_user_point_balance(db, user_id=buyer.id)
    if buyer_balance < product.price_points:
        raise ValueError("Insufficient points to complete the purchase.")

    # 2. Create the transaction record
    db_transaction = transaction_model.Transaction(
        product_id=product.id,
        buyer_id=buyer.id,
        seller_id=product.upcycler_id,
        points_exchanged=product.price_points
    )
    db.add(db_transaction)

    # 3. Update product status
    product.status = ProductStatus.SOLD

    # 4. Adjust points for buyer and seller
    # Deduct points from buyer
    point_service.add_points(
        db,
        user_id=buyer.id,
        reason=PointReason.PRODUCT_PURCHASE,
        description=f"Purchase of '{product.name}'",
        points_override=-product.price_points  # Note the negative value
    )
    # Add points to seller
    point_service.add_points(
        db,
        user_id=product.upcycler_id,
        reason=PointReason.PRODUCT_SALE,
        description=f"Sale of '{product.name}'",
        points_override=product.price_points
    )

    # 5. Commit all changes to the database
    db.commit()
    db.refresh(db_transaction)

    return db_transaction