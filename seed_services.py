from database.db import SessionLocal, engine, Base
from database.models.service import Service

Base.metadata.create_all(bind=engine)

db = SessionLocal()

services = [
    Service(
        name="Permiso de circulación",
        description="Paga o renueva el permiso de circulación de tu vehículo.",
        category="pagos",
        url="https://mlobarnechea.custhelp.com/app/permisos",
        keywords="permiso,auto,patente,vehiculo,pagar"
    ),
    Service(
        name="Becas deportivas",
        description="Postula a becas municipales deportivas.",
        category="beneficios",
        url="https://mlobarnechea.custhelp.com/app/becas",
        keywords="beca,deporte,beneficio,postular"
    ),
    Service(
        name="Eventos culturales",
        description="Revisa eventos y actividades culturales de la comuna.",
        category="eventos",
        url="https://mlobarnechea.custhelp.com/app/eventos",
        keywords="evento,actividad,panorama,concierto,festival"
    ),
]

db.add_all(services)
db.commit()
db.close()
