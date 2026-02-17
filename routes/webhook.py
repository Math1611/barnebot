from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    body = await request.body()

    if not body:
        print("POST sin body")
        return {"status": "empty body"}

    data = await request.json()
    print("DATA RECIBIDA:", data)

    return {"status": "ok"}
