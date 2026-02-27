from fastapi import APIRouter, Request
from database.db import SessionLocal
from services.flow import handle_user_message
import os 

router = APIRouter()

@router.get("/webhook")
def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.verify_token") == os.getenv("VERIFY_TOKEN"):
        return int(params.get("hub.challenge"))
    return "Token inválido", 403


@router.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    try:
        entries = body.get("entry", [])
        if not entries:
            return {"status": "no entry"}

        changes = entries[0].get("changes", [])
        if not changes:
            return {"status": "no changes"}

        value = changes[0].get("value", [])
        if "messages" not in value:
            return {"status": "notification ignored"}

        message_data = value["messages"][0]
        phone = message_data.get("from")
        
        text = get_message_text(message_data)

        if text == "mensaje_no_identificado":
            return {"status": "unidentified message type"}

        db = SessionLocal()
        try:
            await handle_user_message(db, phone, text)
        finally:
            db.close()

    except Exception as e:
        print(f"❌ Error en webhook: {type(e).__name__} - {e}")

    return {"status": "ok"}

def get_message_text(message: dict) -> str:
    """Extrae el ID si es un botón (para lógica) o el texto si es mensaje directo."""
    if "text" in message:
        return message["text"]["body"]
    
    if "interactive" in message:
        interactive = message["interactive"]
        if "button_reply" in interactive:
            return interactive["button_reply"]["id"]
        if "list_reply" in interactive:
            return interactive["list_reply"]["id"]
            
    return "mensaje_no_identificado"