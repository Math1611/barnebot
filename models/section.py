from sqlalchemy import Column, Integer, String, Boolean, Text
from database.db import Base

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    keywords = Column(String, nullable=False)
    short_description = Column(Text, nullable=False)   
    url = Column(String, nullable=True)                
    active = Column(Boolean, default=True)
