from fastapi import APIRouter, Request
from services.flow import handle_button, handle_text

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    message = data["message"]

    phone = message["from"]

    # texto
    if message["type"] == "text":
        text = message["text"]["body"]
        await handle_text(phone, text)

    # botón
    elif message["type"] == "button":
        button_id = message["button"]["payload"]
        await handle_button(phone, button_id)

    return {"status": "ok"}
