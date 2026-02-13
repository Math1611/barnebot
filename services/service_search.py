from database.db import SessionLocal
from database.models.service import Service
from database.db import SessionLocal
from database.models.service import Service
from sqlalchemy import distinct

def get_categories():
    db = SessionLocal()
    cats = db.query(distinct(Service.category)).all()
    db.close()
    return [c[0] for c in cats]


def search_service(text: str):
    db = SessionLocal()

    text = text.lower()

    services = db.query(Service).all()

    for s in services:
        if any(word in text for word in s.keywords.split(",")):
            return s

    return None

def get_services_by_category(category):
    db = SessionLocal()
    items = db.query(Service).filter(Service.category == category).all()
    db.close()
    return items
