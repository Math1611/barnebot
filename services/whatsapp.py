import requests
import os

WA_TOKEN = os.getenv("WA_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def send_whatsapp_message(to, message):

    if len(message) > 4000:
        message = message[:3997] + "..."

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def send_interactive_whatsapp_message(to, payload):
    """
    Esta función envía el JSON complejo que definimos en flow.py 
    para mostrar los botones de idioma.
    """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }

    payload["to"] = to

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Error API WhatsApp: {response.text}")
        
    return response.json()