from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    return {"status": "ok"}
