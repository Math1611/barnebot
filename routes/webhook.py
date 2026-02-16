from fastapi import APIRouter, Request
from services.flow import handle_text, handle_button

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return {"status": "no messages"}

        message = value["messages"][0]
        phone = message["from"]

        if message["type"] == "text":
            text = message["text"]["body"]
            await handle_text(phone, text)


        elif message["type"] == "interactive":
            button_id = message["interactive"]["button_reply"]["id"]
            await handle_button(phone, button_id)

        return {"status": "ok"}

    except Exception as e:
        print("🔥 ERROR WEBHOOK:", e)
        return {"status": "error"}
