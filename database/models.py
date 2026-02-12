from sqlalchemy import Column, String
from database.db import Base


class User(Base):
    __tablename__ = "users"

    phone = Column(String, primary_key=True, index=True)
    language = Column(String, default="es")
