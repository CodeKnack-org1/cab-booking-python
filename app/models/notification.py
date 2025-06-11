from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Notification(Base):
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"))
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    notification_type = Column(String)  # email, sms, push
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notifications") 