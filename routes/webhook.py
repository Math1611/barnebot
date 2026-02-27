from fastapi import APIRouter, Request
from database.db import SessionLocal
from services.flow import handle_user_message
import os 

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    try:
        # 1. Validación de seguridad: Verificar que sea un mensaje de usuario
        # Esto evita el error 'messages' al ignorar notificaciones de entrega/lectura
        entries = body.get("entry", [])
        if not entries:
            return {"status": "no entry"}

        changes = entries[0].get("changes", [])
        if not changes:
            return {"status": "no changes"}

        value = changes[0].get("value", [])
        if "messages" not in value:
            # Si no hay 'messages', es una notificación de sistema (read, delivered, etc.)
            return {"status": "notification ignored"}

        # 2. Extraer datos con seguridad
        message_data = value["messages"][0]
        phone = message_data.get("from")
        
        # Usamos tu función get_message_text para manejar botones e interactivos
        text = get_message_text(message_data)

        if text == "mensaje_no_identificado":
            return {"status": "unidentified message type"}

        db = SessionLocal()
        try:
            # 3. Procesar el mensaje
            await handle_user_message(db, phone, text)
        finally:
            db.close()

    except Exception as e:
        # Imprime el error exacto para depuración
        print(f"❌ Error en webhook: {type(e).__name__} - {e}")

    return {"status": "ok"}

def get_message_text(message: dict) -> str:
    """Extrae el ID si es un botón (para lógica) o el texto si es mensaje directo."""
    if "text" in message:
        return message["text"]["body"]
    
    if "interactive" in message:
        interactive = message["interactive"]
        # Priorizamos el ID del botón para el ruteo en flow.py
        if "button_reply" in interactive:
            return interactive["button_reply"]["id"]  # Cambiado: devuelve 'lang_es' o 'lang_en'
        if "list_reply" in interactive:
            return interactive["list_reply"]["id"]
            
    return "mensaje_no_identificado"