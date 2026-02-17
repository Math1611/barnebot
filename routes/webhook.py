from fastapi import APIRouter, Request
import requests
import os

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

        # 🔹 Enviar respuesta
        token = os.getenv("WA_TOKEN")
        phone_number_id = os.getenv("PHONE_NUMBER_ID")

        url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": f"Recibí tu mensaje: {texto} 🚀"}
        }

        response = requests.post(url, headers=headers, json=payload)
        print("Respuesta de Meta:", response.text)

    except Exception as e:
        print("No es un mensaje válido:", e)
        return {"status": "not a message event"}

    return {"status": "ok"}
