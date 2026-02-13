from services.whatsapp_service import send_buttons, send_text
from services.service_search import get_categories
from services.translations.i18n import t
from services.intent import detect_intent

from database.db import SessionLocal
from database.models.user import User
from database.models.service import Service


# =========================
# USER / DB
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
        t("menu.welcome", user.language),
        buttons + [
            {"id": "language", "title": t("menu.language", user.language)}
        ]
    )


# =========================
# BOTONES
# =========================

async def handle_button(phone: str, button_id: str):

    user, db = get_user(phone)

    try:

        if button_id == "menu":
            await send_main_menu(user)

        # 🔹 categorías dinámicas
        elif button_id.startswith("cat_"):
            category = button_id.replace("cat_", "")

            services = (
                db.query(Service)
                .filter(Service.category == category)
                .all()
            )

            buttons = [
                {"type": "url", "title": s.name, "url": s.url}
                for s in services
            ]

            await send_buttons(
                user.phone,
                f"📂 {category.capitalize()}",
                buttons
            )

        # 🔹 idioma
        elif button_id == "language":
            await send_buttons(
                user.phone,
                t("lang.select", user.language),
                [
                    {"id": "lang_es", "title": "Español"},
                    {"id": "lang_en", "title": "English"},
                ]
            )

        elif button_id == "lang_es":
            user.language = "es"
            db.commit()
            await send_text(user.phone, "Idioma cambiado a Español 🇪🇸")
            await send_main_menu(user)

        elif button_id == "lang_en":
            user.language = "en"
            db.commit()
            await send_text(user.phone, "Language changed to English 🇺🇸")
            await send_main_menu(user)

        else:
            await send_main_menu(user)

    finally:
        db.close()


# =========================
# TEXTO LIBRE + IA
# =========================

async def handle_text(phone: str, text: str):

    user, db = get_user(phone)

    try:

        # 🔹 detectar intención con IA/reglas
        service_key = detect_intent(text)

        if service_key:
            service = (
                db.query(Service)
                .filter(Service.key == service_key)
                .first()
            )

            if service:
                await send_buttons(
                    user.phone,
                    f"📌 {service.name}\n{service.description}",
                    [
                        {
                            "type": "url",
                            "title": t("open_service", user.language),
                            "url": service.url
                        }
                    ]
                )
                return

        # 🔹 fallback
        await send_text(
            user.phone,
            t("not_found", user.language)
        )

        await send_main_menu(user)

    finally:
        db.close()