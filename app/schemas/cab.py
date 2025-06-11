from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.cab import VehicleType

class CabBase(BaseModel):
    vehicle_type: VehicleType
    plate_number: str
    model: str
    color: str
    year: str

class CabCreate(CabBase):
    pass

class CabUpdate(CabBase):
    vehicle_type: Optional[VehicleType] = None
    plate_number: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[str] = None

class Cab(CabBase):
    id: str
    driver_id: str

    class Config:
        from_attributes = True 