from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    text = Column(String)
    direction = Column(String)  # incoming / outgoing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
