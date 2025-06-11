from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentStatus, PaymentMethod

class PaymentBase(BaseModel):
    booking_id: str
    amount: float
    payment_method: PaymentMethod

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    booking_id: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    status: Optional[PaymentStatus] = None

class Payment(PaymentBase):
    id: str
    user_id: str
    status: PaymentStatus
    transaction_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 