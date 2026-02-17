from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        print("DATA RECIBIDA:", data)
    except Exception as e:
        print("No se pudo leer JSON:", e)
        return {"status": "no json received"}

    return {"status": "ok"}
