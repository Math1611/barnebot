import httpx
from config import WA_TOKEN, PHONE_NUMBER_ID

BASE_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"


# =========================
# TEXTO SIMPLE
# =========================
async def send_text(to: str, message: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {WA_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message},
            },
        )


# =========================
# BOTONES
# =========================
async def send_buttons(to: str, message: str, buttons: list):
    async with httpx.AsyncClient() as client:

        formatted_buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": b["id"],
                    "title": b["title"]
                }
            }
            for b in buttons
        ]

        await client.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {WA_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": message},
                    "action": {
                        "buttons": formatted_buttons
                    }
                },
            },
        )
