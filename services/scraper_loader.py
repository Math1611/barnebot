from database.db import SessionLocal
from models.document import Document
from services.vector_service import generate_embedding
from sqlalchemy import text

def load_all_pdf_data():
    db = SessionLocal()
    try:
        print("🚀 Iniciando carga masiva de BarneBot...")
        
        data = [
            # PÁGINA 1: TRÁNSITO
            {"title": "Atención al Vecino", "cat": "General", "url": "https://mlobarnechea.custhelp.com/app/formularios/Solicitudes%20Vecinos", "content": "Formularios y solicitudes generales para vecinos de Lo Barnechea."},
            {"title": "Licencia de Conducir: Requisitos", "cat": "Tránsito", "url": "https://lobarnechea.cl/vecinos/tramites-y-solicitudes/licencia-de-conducir/requisitos/", "content": "Requisitos para obtener o renovar la licencia de conducir."},
            {"title": "Agenda tu Hora Licencia", "cat": "Tránsito", "url": "https://lobarnechea.saltala.com/#/servicios/unit-277", "content": "Reserva de hora para trámites de licencia de conducir."},
            {"title": "Permiso de Circulación: Pagar", "cat": "Tránsito", "url": "https://pago.smc.cl/pagoPCVv2/muni/lo_barnechea.aspx", "content": "Portal de pago online del permiso de circulación."},
            
            # PÁGINA 2: PATENTES
            {"title": "Patentes Municipales", "cat": "Comercial", "url": "https://mlobarnechea.custhelp.com/app/tramites/patentes_municipales", "content": "Trámites de patente comercial, profesional, alcoholes y microempresa familiar."},
            
            # PÁGINA 3: OBRAS
            {"title": "Obras Municipales: Certificados", "cat": "Obras", "url": "https://lobarnechea.filedom.cl/index.php?parent=Direcci%C3%B3n%20de%20Obras%20Municipales", "content": "Certificados online de la dirección de obras municipales DOM."},
            
            # PÁGINA 4: JUZGADO
            {"title": "Demandas por Choque", "cat": "JPL", "url": "https://mlobarnechea.custhelp.com/app/answers/detail/a_id/77/incidents.c$tipo_atencion/221", "content": "Presentación de demandas por daños en choque en el Juzgado de Policía Local."},
            {"title": "Pago de Partes y Multas", "cat": "JPL", "url": "https://pago.smc.cl/pagoRMNPv2/muni/lo_barnechea.aspx", "content": "Pago online de partes, multas de tránsito y tag."},
            
            # PÁGINA 5: PAGOS Y BENEFICIOS
            {"title": "Derecho de Aseo", "cat": "Pagos", "url": "https://pago.smc.cl/pagoASEOv2/muni/lo_barnechea.aspx", "content": "Pago de aseo domiciliario y sobreproducción de basura."},
            {"title": "Beneficios Sociales", "cat": "Social", "url": "https://mlobarnechea.custhelp.com/app/postulaciones/inicio/a_id/47", "content": "Postulaciones a beneficios sociales, subsidios y ayudas municipales."},
            
            # PÁGINA 6: SALUD Y SEGURIDAD
            {"title": "Vacunación 2025", "cat": "Salud", "url": "https://lobarnechea.cl/Noticias/influenza-y-covid-lo-barnechea-comenzo-la-campana-de-vacunacion-2025", "content": "Campaña de vacunación Influenza y COVID 2025."},
            {"title": "Seguridad 1405", "cat": "Seguridad", "url": "https://lobarnechea.cl/seguridad/telefono-de-emergencias-1405/", "content": "Teléfono de emergencias 1405 y atención a víctimas."},
            {"title": "Encarga tu Casa", "cat": "Seguridad", "url": "https://lobarnechea.cl/seguridad/encarga-tu-casa/", "content": "Programa municipal para encargar la casa durante vacaciones o viajes."},
            
            # PÁGINA 7: ESTADO SOLICITUD
            {"title": "Estado de Solicitud", "cat": "General", "url": "https://mlobarnechea.custhelp.com/app/estado_solicitudes", "content": "Consulta el estado de tus solicitudes en la municipalidad."}
        ]

        for item in data:
            emb = generate_embedding(item["content"])
            doc = Document(
                title=item["title"],
                content=item["content"],
                url=item["url"],
                category=item["cat"],
                embedding=emb
            )
            db.add(doc)
            print(f"✅ Agregado: {item['title']}")
        
        db.commit() # ¡ESTO ES LO MÁS IMPORTANTE!
        print("✨ ¡Todo guardado en la base de datos!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_all_pdf_data()