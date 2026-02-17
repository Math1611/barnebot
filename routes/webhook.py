from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    body = await request.body()

    if not body:
        return {"status": "empty body"}

    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = message["from"]
        texto = message["text"]["body"]

        print("Número:", numero)
        print("Mensaje:", texto)

    except Exception as e:
        print("No es un mensaje:", e)
        return {"status": "not a message event"}

    return {"status": "ok"}
