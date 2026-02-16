from sqlalchemy import Column, Integer, String, Text
from database.db import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)

    url = Column(Text, nullable=False)

    keywords = Column(Text, nullable=False)