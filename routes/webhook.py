from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.message import Message
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

        db: Session = SessionLocal()

        # 🔹 Guardar mensaje entrante
        incoming = Message(
            phone_number=numero,
            text=texto,
            direction="incoming"
        )
        db.add(incoming)
        db.commit()

        # 🔹 Preparar respuesta
        respuesta_texto = f"Recibí tu mensaje: {texto} 🚀"

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
            "text": {"body": respuesta_texto}
        }

        requests.post(url, headers=headers, json=payload)

        # 🔹 Guardar mensaje saliente
        outgoing = Message(
            phone_number=numero,
            text=respuesta_texto,
            direction="outgoing"
        )
        db.add(outgoing)
        db.commit()

        db.close()

    except Exception as e:
        print("Error:", e)
        return {"status": "error"}

    return {"status": "ok"}
