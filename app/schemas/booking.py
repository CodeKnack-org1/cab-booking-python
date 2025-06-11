from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.booking import BookingStatus

class BookingBase(BaseModel):
    pickup_location: str
    dropoff_location: str
    scheduled_time: Optional[datetime] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None
    status: Optional[BookingStatus] = None
    fare: Optional[float] = None
    distance: Optional[float] = None
    duration: Optional[float] = None

class Booking(BookingBase):
    id: str
    user_id: str
    driver_id: Optional[str] = None
    cab_id: Optional[str] = None
    status: BookingStatus
    fare: Optional[float] = None
    distance: Optional[float] = None
    duration: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 