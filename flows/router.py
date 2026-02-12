from services.whatsapp import send_buttons, send_text


async def handle_button(user, btn_id):

    if btn_id == "menu":
        send_buttons(user, "¿Qué necesitas?", [
            {"id": "horarios", "title": "Horarios"},
            {"id": "ubicaciones", "title": "Ubicaciones"},
            {"id": "clima", "title": "Clima"},
        ])

    elif btn_id == "clima":
        send_text(user, "🌤️ 24°C Parcialmente nublado")

    elif btn_id == "horarios":
        send_text(user, "🕘 Lunes a Viernes 8:30–14:00")

    elif btn_id == "ubicaciones":
        send_text(user, "📍 https://maps.google.com/...")

    else:
        send_text(user, "Usa los botones 👇")
