import unicodedata
import re
from database.db import SessionLocal
from models.user import User
from models.message import Message
from services.whatsapp import send_whatsapp_message, send_interactive_whatsapp_message
from services.menus import main_menu, main_menu_en
from services.rag_service import RAGService 

rag_handler = RAGService()

HELP_KEYWORDS = ["ayuda", "ayudame", "help", "no entiendo"]
GREETING_KEYWORDS = ["hola", "buenas", "hi", "hello"]
MENU_KEYWORDS = ["menu", "inicio"]

# ======================================================
# HELPERS
# ======================================================

def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def get_or_create_user(db, phone):
    user = db.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone, language="es", state="main_menu")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def is_menu_request(text):
    return any(kw in text for kw in GREETING_KEYWORDS) or text in MENU_KEYWORDS

def is_help_request(text):
    return any(kw in text for kw in HELP_KEYWORDS)

# ======================================================
# ENVÍO Y ALMACENAMIENTO
# ======================================================

async def send_and_store(db, phone, text):
    send_whatsapp_message(phone, text)
    new_msg = Message(phone_number=phone, text=text, direction="outgoing")
    db.add(new_msg)
    db.commit()

async def send_language_selection(phone):
    data = {
        "messaging_product": "whatsapp",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "¡Hola! Bienvenido a BarneBot 🏡\n\nPor favor, selecciona tu idioma para comenzar:\n\nPlease select your language to begin:"
            },
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "lang_es", "title": "Español 🇨🇱"}},
                    {"type": "reply", "reply": {"id": "lang_en", "title": "English 🇺🇸"}}
                ]
            }
        }
    }
    send_interactive_whatsapp_message(phone, data)

# ======================================================
# STATE HANDLERS 
# ======================================================

async def handle_main_menu(db, user, phone, text):
    keyword_map = {
        "1": "licencia de conducir trámites tránsito vehículos",
        "2": "pagos online patentes aseo multas tag contribuciones",
        "3": "beneficios sociales registro social hogares farmacia salud vacunas",
        "4": "seguridad emergencias 1405 vigilancia",
        "5": "reciclaje retiro basura escombros medioambiente"
    }

    if text in keyword_map:
        query = keyword_map[text]
        ai_response = await rag_handler.process_query(db, query, user.language)
        return await send_and_store(db, phone, ai_response)
    
    menu_content = main_menu_en() if user.language == "en" else main_menu()
    return await send_and_store(db, phone, menu_content)

# ======================================================
# ENTRYPOINT PRINCIPAL
# ======================================================

async def handle_user_message(db, phone: str, text: str):
    raw_text = text.strip()
    normalized_text = normalize_text(raw_text)
    user = get_or_create_user(db, phone)

    if raw_text == "lang_es":
        user.language = "es"
        user.state = "main_menu"
        db.commit()
        return await send_and_store(db, phone, "¡Genial! 🇨🇱\n" + main_menu())

    if raw_text == "lang_en":
        user.language = "en"
        user.state = "main_menu"
        db.commit()
        return await send_and_store(db, phone, "Great! 🇺🇸\n" + main_menu_en())

    if is_menu_request(normalized_text):
        return await send_language_selection(phone)

    if is_help_request(normalized_text):
        msg = "Escriba un número o su pregunta. / Type a number or your question. 🤓"
        return await send_and_store(db, phone, msg)

    if user.state == "main_menu" and raw_text.isdigit():
        return await handle_main_menu(db, user, phone, raw_text)

    print(f"🔍 Buscando en PDF para: {raw_text}")
    ai_response = await rag_handler.process_query(db, raw_text, user.language)
    return await send_and_store(db, phone, ai_response)