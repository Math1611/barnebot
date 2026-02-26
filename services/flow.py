from database.db import SessionLocal
from models.user import User
from models.message import Message
from services.whatsapp import send_whatsapp_message
from services.menus import (
    main_menu,
    tramites_menu,
    transito_tramites_menu,
    licencias_menu,
    info_licencia_primera_vez,
    info_renovacion_licencia,
    pagos_online
)

import unicodedata
import re
from services.rag_service import RAGService # Importamos el servicio centralizado
from services.vector_service import search_vector_database

# Instanciamos el servicio RAG una sola vez
rag_handler = RAGService()

# ==============================
# KEYWORDS
# ==============================

HELP_KEYWORDS = ["ayuda", "ayudame", "help", "no entiendo"]
GREETING_KEYWORDS = ["hola", "buenas", "hi", "hello"]
MENU_KEYWORDS = ["menu", "inicio"]

# ======================================================
# ENTRYPOINT PRINCIPAL
# ======================================================

async def handle_user_message(db, phone: str, text: str):
    raw_text = text.strip()
    normalized_text = normalize_text(raw_text)

    user = get_or_create_user(db, phone)

    # 1. ATAJOS GLOBALES (Saludos y Menú)
    if is_menu_request(normalized_text):
        return await respond_with_menu(db, phone, user)

    if is_help_request(normalized_text):
        return await send_and_store(
            db,
            phone,
            "🤝 Puedes navegar usando los números del menú.\nEscribe *menu* para volver al inicio."
        )

    # 2. MÁQUINA DE ESTADOS (Navegación por números)
    state_handlers = {
        "main_menu": handle_main_menu,
        "tramites_menu": handle_tramites_menu,
        "transito_menu": handle_transito_menu,
        "licencias_menu": handle_licencias_menu,
    }

    handler = state_handlers.get(user.state)

    # Si el mensaje es un número y estamos en un estado válido -> Navegar
    if handler and raw_text.isdigit():
        return await handler(db, user, phone, raw_text)

    # 3. RAG MUNICIPAL (Buscador Inteligente para preguntas abiertas)
    # Si no es un comando de menú ni un número, consultamos la base de datos del PDF
    print(f"🔍 Buscando en PDF para: {raw_text}")
    
    ai_response = await rag_handler.process_query(db, raw_text)
    
    return await send_and_store(db, phone, ai_response)


# ======================================================
# STATE HANDLERS
# ======================================================

async def handle_main_menu(db, user, phone, text):
    options = {
        "1": ("tramites_menu", tramites_menu),
        "2": ("pagos_menu", pagos_online),
    }
    return await process_options(db, user, phone, text, options, main_menu)

async def handle_tramites_menu(db, user, phone, text):
    options = {
        "1": ("transito_menu", transito_tramites_menu),
        "0": ("main_menu", main_menu),
    }
    return await process_options(db, user, phone, text, options, tramites_menu)

async def handle_transito_menu(db, user, phone, text):
    options = {
        "1": ("licencias_menu", licencias_menu),
        "0": ("tramites_menu", tramites_menu),
    }
    return await process_options(db, user, phone, text, options, transito_tramites_menu)

async def handle_licencias_menu(db, user, phone, text):
    options = {
        "1": ("licencias_menu", info_licencia_primera_vez),
        "2": ("licencias_menu", info_renovacion_licencia),
        "0": ("transito_menu", transito_tramites_menu),
    }
    return await process_options(db, user, phone, text, options, licencias_menu)

# ======================================================
# CORE OPTION PROCESSOR
# ======================================================

async def process_options(db, user, phone, text, options, default_menu_func):
    if text in options:
        new_state, menu_func = options[text]
        user.state = new_state
        db.commit()
        return await send_and_store(db, phone, menu_func())

    # Si presiona un número que no está en las opciones, re-enviar menú actual
    return await send_and_store(db, phone, default_menu_func())

# ======================================================
# RESPUESTAS Y ALMACENAMIENTO
# ======================================================

async def respond_with_menu(db, phone, user):
    user.state = "main_menu"
    db.commit()
    return await send_and_store(db, phone, main_menu())

async def send_and_store(db, phone, text):
    # Enviar a WhatsApp
    send_whatsapp_message(phone, text)

    # Guardar en historial
    new_msg = Message(
        phone_number=phone,
        text=text,
        direction="outgoing"
    )
    db.add(new_msg)
    db.commit()

# ======================================================
# HELPERS
# ======================================================

def get_or_create_user(db, phone):
    user = db.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone, language="es", state="main_menu")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def is_menu_request(text):
    return text in GREETING_KEYWORDS or text in MENU_KEYWORDS

def is_help_request(text):
    return any(kw in text for kw in HELP_KEYWORDS)