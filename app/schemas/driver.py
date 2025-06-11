from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DriverBase(BaseModel):
    license_number: str
    current_location: Optional[str] = None

class DriverCreate(DriverBase):
    pass

class DriverUpdate(DriverBase):
    license_number: Optional[str] = None
    is_available: Optional[bool] = None
    current_location: Optional[str] = None

class Driver(DriverBase):
    id: str
    user_id: str
    is_available: bool
    rating: float
    total_rides: int
    total_earnings: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 