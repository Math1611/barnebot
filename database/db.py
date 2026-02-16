from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 🔹 Construir la URL correctamente con SSL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

# 🔹 Crear engine
engine = create_engine(DATABASE_URL)

# 🔹 Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Base declarativa
Base = declarative_base()
