from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class VehicleType(str, enum.Enum):
    SEDAN = "sedan"
    SUV = "suv"
    LUXURY = "luxury"
    VAN = "van"

class Cab(Base):
    id = Column(String, primary_key=True, index=True)
    driver_id = Column(String, ForeignKey("driver.id"))
    vehicle_type = Column(Enum(VehicleType))
    plate_number = Column(String, unique=True)
    model = Column(String)
    color = Column(String)
    year = Column(String)
    
    # Relationships
    driver = relationship("Driver", back_populates="cabs")
    bookings = relationship("Booking", back_populates="cab") 