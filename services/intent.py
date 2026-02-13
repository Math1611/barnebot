from typing import Optional

INTENT_MAP = {
    # 🚗 Permiso circulación
    "permiso": "permiso_circulacion",
    "auto": "permiso_circulacion",
    "patente": "permiso_circulacion",
    "vehiculo": "permiso_circulacion",

    # 🪪 Licencia conducir
    "licencia": "licencia_conducir",
    "conducir": "licencia_conducir",

    # 💸 Multas
    "multa": "pago_multas",
    "multas": "pago_multas",
    "parte": "pago_multas",

    # 🏠 Aseo
    "aseo": "derecho_aseo",
    "basura": "derecho_aseo",

    # 📄 Certificados
    "certificado": "certificados",
    "residencia": "certificados",
}


def normalize(text: str) -> str:
    """
    Limpia texto:
    - minúsculas
    - quita tildes
    """
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
    }

    text = text.lower()

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def detect_intent(text: str) -> Optional[str]:
    """
    Retorna service.key o None
    """
    text = normalize(text)

    for word, service_key in INTENT_MAP.items():
        if word in text:
            return service_key

    return None