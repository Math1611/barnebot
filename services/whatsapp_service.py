import httpx
from config import WA_TOKEN, PHONE_NUMBER_ID

URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"


async def send_buttons(to: str, text: str, buttons: list):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text},
            "action": {
                "buttons": buttons
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(URL, headers=headers, json=payload)
        print("META RESPONSE:", r.status_code, r.text)
