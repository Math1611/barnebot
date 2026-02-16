import requests
from config import WA_TOKEN, PHONE_NUMBER_ID

BASE_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"


def send_payload(payload):
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    requests.post(BASE_URL, headers=headers, json=payload)


def send_text(to, text):
    send_payload({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    })


def send_buttons(to, text, buttons):
    send_payload({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": b} for b in buttons
                ]
            }
        }
    })
