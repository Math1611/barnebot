from fastapi import FastAPI
from routes.webhook import router as webhook_router
from database.db import Base, engine
from database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Municipal WhatsApp Bot")

app.include_router(webhook_router)

@app.get("/")
def root():
    return {"status": "running"}