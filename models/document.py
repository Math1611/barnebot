from sqlalchemy import Column, Integer, String, Text
from database.db import Base
from pgvector.sqlalchemy import Vector

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    embedding = Column(Vector(384), nullable=False)