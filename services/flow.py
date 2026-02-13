from services.whatsapp_service import send_buttons, send_text
from services.service_search import search_service
from services.translations.i18n import t
from database.db import SessionLocal
from database.models.user import User
from services.service_search import get_categories
from services.intent import detect_intent
from database.models.service import Service


# =========================
# UTIL
# =========================

def get_user(phone: str):
    db = SessionLocal()
    user = db.query(User).filter_by(phone=phone).first()

    if not user:
        user = User(phone=phone, language="es")
        db.add(user)
        db.commit()
        db.refresh(user)

    return user, db



# =========================
# MENÚ PRINCIPAL
# =========================


async def send_main_menu(user):

    categories = get_categories()
    buttons = [
        {"id": f"cat_{c}", "title": c.capitalize()}
        for c in categories
    ]

    await send_buttons(
        user.phone,
        "¿En qué te ayudo?",
        buttons
    )

    await send_buttons(
        user.phone,
        t("menu.welcome", user.language),
        [
            {"id": "tramites", "title": t("menu.tramites", user.language)},
            {"id": "pagos", "title": t("menu.pagos", user.language)},
            {"id": "beneficios", "title": t("menu.beneficios", user.language)},
            {"id": "eventos", "title": t("menu.eventos", user.language)},
            {"id": "language", "title": t("menu.language", user.language)},
        ]
    )


# =========================
# BOTONES
# =========================



async def handle_button(phone: str, button_id: str):
    
    user, db = get_user(phone)

    
    if button_id == "menu":
        await send_main_menu(user)

    elif button_id.startswith("cat_"):
        category = button_id.replace("cat_", "")
        await send_category_services(user, category)

    elif button_id == "tramites":
        await send_text(user.phone, t("ask.tramite", user.language))

    elif button_id == "pagos":
        await send_text(user.phone, t("ask.pagos", user.language))

    elif button_id == "beneficios":
        await send_text(user.phone, t("ask.beneficios", user.language))

    elif button_id == "eventos":
        await send_text(user.phone, t("ask.eventos", user.language))

    elif button_id == "language":
        await send_buttons(
            user.phone,
            t("lang.select", user.language),
            [
                {"id": "lang_es", "title": t("lang.es", user.language)},
                {"id": "lang_en", "title": t("lang.en", user.language)},
            ]
        )

    elif button_id == "lang_es":
        user.language = "es"
        db.commit()
        await send_text(user.phone, t("lang.changed", "es"))
        await send_main_menu(user)

    elif button_id == "lang_en":
        user.language = "en"
        db.commit()
        await send_text(user.phone, t("lang.changed", "en"))
        await send_main_menu(user)

    db.close()


# =========================
# TEXTO LIBRE
# =========================

async def handle_text(phone: str, text: str):

    user, db = get_user(phone)

    service = search_service(text)

    if service:
        await send_buttons(
            user.phone,
            f"📌 {service.name}\n{service.description}",
            [
                {
                    "type": "url",
                    "title": "Abrir trámite",
                    "url": service.url
                }
            ]
        )
    else:
        await send_text(user.phone, t("not_found", user.language))
        await send_main_menu(user)

    db.close()


def handle_text(user, message):
    intent = detect_intent(message)

    if intent:
        service = get_service_by_key(intent)
        return send_service(service)

    return send_menu()

def handle_text(user, message, db):

    # 🔹 detectar intención
    service_key = detect_intent(message)

    if service_key:
        service = (
            db.query(Service)
            .filter(Service.key == service_key)
            .first()
        )

        if service:
            return {
                "text": service.description,
                "buttons": [
                    {
                        "type": "url",
                        "title": "Ir al trámite",
                        "url": service.url
                    }
                ]
            }

    # 🔹 fallback menú
    return {
        "text": "Elige una opción 👇",
        "buttons": [
            {"type": "reply", "title": "Permiso circulación", "id": "permiso_circulacion"},
            {"type": "reply", "title": "Licencia conducir", "id": "licencia_conducir"},
            {"type": "reply", "title": "Multas", "id": "pago_multas"},
        ]
    }
