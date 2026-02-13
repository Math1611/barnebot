from fastapi import FastAPI
from routes.webhook import router as webhook_router
from database.db import Base, engine
from database.db import engine, Base
from database import models
import os
import uvicorn

app = FastAPI()
app.include_router(webhook_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )


Base.metadata.create_all(bind=engine)

app.include_router(webhook_router)

@app.get("/")
def root():
    return {"status": "running"}
    
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
