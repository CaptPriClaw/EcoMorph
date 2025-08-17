# backend/app/schemas/transaction_schema.py
from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    product_id: int
    points_exchanged: int

class Transaction(TransactionBase):
    id: int
    buyer_id: int
    seller_id: int
    transaction_time: datetime

    class Config:
        from_attributes = True # <-- CORRECTED