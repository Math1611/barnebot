from fastapi import FastAPI
from routes.webhook import router as webhook_router
from database.db import Base, engine
from models.user import User
from models.service import Service
from models.message import Message
import os
import uvicorn
from contextlib import asynccontextmanager
from models.section import Section



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(webhook_router)

@app.get("/")
def root():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
