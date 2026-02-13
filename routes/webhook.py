from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from config import VERIFY_TOKEN
from services.flow import handle_button, handle_text

router = APIRouter()


@router.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return PlainTextResponse(params.get("hub.challenge"))

    return {"error": "verification failed"}


@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user = msg["from"]

        if msg["type"] == "text":
            text = msg["text"]["body"]
            await handle_text(user, text)

        elif msg["type"] == "interactive":
            button_id = msg["interactive"]["button_reply"]["id"]
            await handle_button(user, button_id)

    except Exception as e:
        print("ERROR:", e)

    return {"ok": True}
