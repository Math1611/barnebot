from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from config import VERIFY_TOKEN
from services.flow import handle_button

router = APIRouter()


@router.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    challenge = params.get("hub.challenge")
    token = params.get("hub.verify_token")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return {"error": "verification failed"}


@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user = msg["from"]

        # ✅ texto → menú automático
        if msg["type"] == "text":
            await handle_button(user, "menu")

        # ✅ botones
        elif msg["type"] == "interactive":
            btn_id = msg["interactive"]["button_reply"]["id"]
            await handle_button(user, btn_id)

        else:
            await handle_button(user, "menu")

    except Exception as e:
        print("ERROR:", e)

    return {"ok": True}
