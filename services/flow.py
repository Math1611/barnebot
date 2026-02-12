from services.whatsapp_service import send_buttons
from services.weather_service import get_weather
from services.user_service import get_or_create_user, set_language


async def handle_button(user: str, btn_id: str):

    user_data = get_or_create_user(user)
    lang = user_data["language"]


    is_en = lang == "en"
    back = "⬅️ Back" if is_en else "⬅️ Volver"


    # =================================================
    # MENÚ PRINCIPAL
    # =================================================
    if btn_id == "menu":

        text = (
            "👋 Hi! I'm *Barnebot*, Lo Barnechea virtual assistant.\nUse the buttons below."
            if is_en
            else
            "👋 ¡Hola! Soy *Barnebot*, asistente virtual de Lo Barnechea.\nUsa los botones para continuar."
        )

        await send_buttons(user, text, [
            {"type": "reply", "reply": {"id": "horarios", "title": "🕐 Schedule" if is_en else "🕐 Horarios"}},
            {"type": "reply", "reply": {"id": "ubicaciones", "title": "📍 Locations" if is_en else "📍 Ubicaciones"}},
            {"type": "reply", "reply": {"id": "mas", "title": "➕ More" if is_en else "➕ Más"}},
        ])


    # =================================================
    # HORARIOS
    # =================================================
    elif btn_id == "horarios":

        text = (
            "🕐 Opening hours:\nMon–Fri 8:30–14:00"
            if is_en
            else
            "🕐 Atención municipal:\nLun–Vie 8:30–14:00"
        )

        await send_buttons(user, text, [
            {"type": "reply", "reply": {"id": "menu", "title": back}}
        ])


    # =================================================
    # UBICACIONES
    # =================================================
    elif btn_id == "ubicaciones":

        text = (
            "📍 City Hall location:\nhttps://maps.google.com/?q=municipalidad"
            if is_en
            else
            "📍 Municipalidad:\nhttps://maps.google.com/?q=municipalidad"
        )

        await send_buttons(user, text, [
            {"type": "reply", "reply": {"id": "menu", "title": back}}
        ])


    # =================================================
    # SUBMENÚ MÁS
    # =================================================
    elif btn_id == "mas":

        await send_buttons(
            user,
            "More options:" if is_en else "Más opciones:",
            [
                {"type": "reply", "reply": {"id": "clima", "title": "🌤 Weather" if is_en else "🌤 Clima"}},
                {"type": "reply", "reply": {"id": "idioma", "title": "🌎 Language" if is_en else "🌎 Idioma"}},
                {"type": "reply", "reply": {"id": "faq", "title": "❓ FAQ"}},
            ]
        )


    # =================================================
    # CLIMA
    # =================================================
    elif btn_id == "clima":

        weather = get_weather()

        text = (
            f"🌤 Weather:\n{weather}"
            if is_en
            else
            f"🌤 Clima actual:\n{weather}"
        )

        await send_buttons(user, text, [
            {"type": "reply", "reply": {"id": "mas", "title": back}}
        ])


    # =================================================
    # IDIOMA
    # =================================================
    elif btn_id == "idioma":

        await send_buttons(
            user,
            "🌎 Select language / Selecciona idioma",
            [
                {"type": "reply", "reply": {"id": "lang_es", "title": "🇪🇸 Español"}},
                {"type": "reply", "reply": {"id": "lang_en", "title": "🇺🇸 English"}},
            ]
        )

    elif btn_id == "lang_es":
        set_language(user, "es")
        await handle_button(user, "menu")

    elif btn_id == "lang_en":
        set_language(user, "en")
        await handle_button(user, "menu")


        # =================================================
    # FAQ
    # =================================================
    elif btn_id == "faq":

        is_en = lang == "en"

        text = "Frequently asked questions:" if is_en else "Preguntas frecuentes:"

        await send_buttons(
            user,
            text,
            [
                {"type": "reply", "reply": {"id": "faq_pagos", "title": "💳 Payments" if is_en else "💳 Pagos"}},
                {"type": "reply", "reply": {"id": "faq_permisos", "title": "📄 Permits" if is_en else "📄 Permisos"}},
                {"type": "reply", "reply": {"id": "faq_servicios", "title": "🏛 Services" if is_en else "🏛 Servicios"}},
            ]
        )


    # =================================================
    # FAQ PAG 2
    # =================================================
    elif btn_id == "faq_servicios":

        is_en = lang == "en"

        await send_buttons(
            user,
            "More topics:" if is_en else "Más temas:",
            [
                {"type": "reply", "reply": {"id": "faq_basura", "title": "🗑 Garbage" if is_en else "🗑 Basura"}},
                {"type": "reply", "reply": {"id": "faq_contacto", "title": "📞 Contact" if is_en else "📞 Contacto"}},
                {"type": "reply", "reply": {"id": "faq_volver", "title": "⬅️ Back" if is_en else "⬅️ Volver"}},
            ]
        )


    elif btn_id == "faq_volver":
        await handle_button(user, "faq")


    # =================================================
    # RESPUESTAS
    # =================================================
    elif btn_id == "faq_pagos":

        text = (
            "💳 You can pay online at:\nhttps://lobarnechea.cl/pagos"
            if lang == "en"
            else
            "💳 Puedes pagar en línea en:\nhttps://lobarnechea.cl/pagos"
        )

        await send_buttons(user, text, [{"type": "reply", "reply": {"id": "faq", "title": back}}])


    elif btn_id == "faq_permisos":

        text = (
            "📄 Permits are requested at the Urban Planning Office (DOM)."
            if lang == "en"
            else
            "📄 Los permisos se solicitan en la Dirección de Obras Municipales (DOM)."
        )

        await send_buttons(user, text, [{"type": "reply", "reply": {"id": "faq", "title": back}}])


    elif btn_id == "faq_basura":

        text = (
            "🗑 Garbage collection: Mon, Wed and Fri mornings."
            if lang == "en"
            else
            "🗑 Recolección: lunes, miércoles y viernes en la mañana."
        )

        await send_buttons(user, text, [{"type": "reply", "reply": {"id": "faq_servicios", "title": back}}])


    elif btn_id == "faq_contacto":

        text = (
            "📞 Phone: +56 2 2757 6000\n✉️ contacto@lobarnechea.cl"
            if lang == "en"
            else
            "📞 Teléfono: +56 2 2757 6000\n✉️ contacto@lobarnechea.cl"
        )

        await send_buttons(user, text, [{"type": "reply", "reply": {"id": "faq_servicios", "title": back}}])
