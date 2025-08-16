# backend/app/schemas/transaction_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# These schemas would be used for nested responses to provide more detail.
# from .product_schema import Product
# from .user_schema import User

class TransactionBase(BaseModel):
    product_id: int
    points_exchanged: int


class TransactionCreate(TransactionBase):
    buyer_id: int
    seller_id: int


class Transaction(TransactionBase):
    id: int
    buyer_id: int
    seller_id: int
    transaction_time: datetime

    # For a richer API, you could include the full objects like this:
    # product: Product
    # buyer: User
    # seller: User

    class Config:
        orm_mode = True