def main_menu():
    return """
👋 ¡Hola! Soy BarneBot 🏡
Tu asistente de la Municipalidad de Lo Barnechea.

Puedes preguntarme directamente lo que necesites o usar estos números para guiarte:

1️⃣ *Trámites y Licencias* (Conducir, Permisos)
2️⃣ *Pagos Online* (Patentes, Aseo, Multas)
3️⃣ *Beneficios y Salud* (RSH, Farmacia, Vacunas)
4️⃣ *Seguridad y Emergencias* (1405, SOS)
5️⃣ *Medioambiente* (Reciclaje, Retiro de basura)

O simplemente dime: "¿Cómo saco mi licencia?" o "¿Dónde pago el TAG?" 😊
"""

def main_menu_en():
    return """
👋 Hi! I'm BarneBot 🏡
Your assistant for the Municipality of Lo Barnechea.

You can ask me anything directly or use these numbers as a guide:

1️⃣ *Procedures & Licenses* (Driving, Permits)
2️⃣ *Online Payments* (Vehicle tax, Trash, Fines)
3️⃣ *Benefits & Health* (Social aid, Pharmacy, Vaccines)
4️⃣ *Security & Emergencies* (1405, SOS)
5️⃣ *Environment* (Recycling, Waste collection)

Or just ask: "How do I get my license?" or "Where can I pay my highway toll?" 😊
"""

def estado_de_solicitud(lang="es"):
    if lang == "en":
        return """
🔍 *Request Status*

To check your status, please fill out the following form with your request number:
🔗 https://mlobarnechea.custhelp.com/app/estado_solicitudes
"""
    return """
🔍 *Estado de Solicitud*

Para saber más sobre tu estado, ingresa al siguiente link y completa el formulario con tu número de solicitud:
🔗 https://mlobarnechea.custhelp.com/app/estado_solicitudes
"""