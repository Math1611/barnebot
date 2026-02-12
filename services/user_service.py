from database.db import SessionLocal
from database.models import User


def get_or_create_user(phone: str):

    db = SessionLocal()

    user = db.query(User).filter(User.phone == phone).first()

    if not user:
        user = User(phone=phone, language="es")
        db.add(user)
        db.commit()
        db.refresh(user)

    lang = user.language  # guardamos antes de cerrar

    db.close()

    return {
        "phone": phone,
        "language": lang
    }


def set_language(phone: str, lang: str):

    db = SessionLocal()

    user = db.query(User).filter(User.phone == phone).first()

    if user:
        user.language = lang
        db.commit()

    db.close()
