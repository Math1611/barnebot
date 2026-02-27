from database.db import SessionLocal, engine, Base
from models.document import Document
from services.vector_service import generate_embedding
from sqlalchemy import text

def load_data_final():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("🛠️ Verificando conexión y limpiando tabla...")
        db.execute(text("TRUNCATE TABLE documents"))
        db.commit()

        data_to_load = [
            # 1. TRÁMITES Y TRÁNSITO
            {"title": "Portal de Trámites General", "cat": "Trámites", "url": "https://mlobarnechea.custhelp.com/app/tramites/inicio", "content": "Ver todos los trámites, gestión de documentos municipal, oficina virtual, hacer trámites por internet, listado de servicios generales municipales."},
            {"title": "Atención al Vecino", "cat": "Trámites", "url": "https://mlobarnechea.custhelp.com/app/formularios/Solicitudes%20Vecinos", "content": "Hablar con alguien, mandar reclamo, hacer una consulta, pedir ayuda al vecino, formulario de contacto, sugerencias, reclamos y felicitaciones."},
            {"title": "Licencia de Conducir (Info)", "cat": "Tránsito", "url": "https://mlobarnechea.custhelp.com/app/tramites/transito/licencia_de_conducir", "content": "Sacar la licencia por primera vez, renovar el carnet de manejar, requisitos para conducir, documentos para la licencia, examen médico conductor."},
            {"title": "Examen Teórico Licencia", "cat": "Tránsito", "url": "https://lobarnechea.cl/vecinos/tramites-y-solicitudes/licencia-de-conducir/examen-teorico/", "content": "Estudiar para el examen de conducir, libro del nuevo conductor, preguntas del examen teórico, test de manejo, cuestionario clase B."},
            {"title": "Examen Práctico Licencia", "cat": "Tránsito", "url": "https://lobarnechea.cl/vecinos/tramites-y-solicitudes/licencia-de-conducir/examen-practico/", "content": "Cómo es la prueba de manejo, ruta del examen práctico, qué te piden en el examen de conducir, evaluación en calle."},
            {"title": "Valores Licencias", "cat": "Tránsito", "url": "https://lobarnechea.cl/vecinos/tramites-y-solicitudes/licencia-de-conducir/valores/", "content": "Cuánto cuesta la licencia, precio del trámite de conducir, valor de renovación, pago de derechos municipales de licencia."},
            {"title": "Agenda tu Hora (Sáltala)", "cat": "Tránsito", "url": "https://lobarnechea.saltala.com/#/servicios/unit-277", "content": "Pedir hora, sacar turno, agendar cita para licencia de conducir o atención presencial, reservar cupo, saltala atención."},
            {"title": "Permiso de Circulación", "cat": "Tránsito", "url": "https://mlobarnechea.custhelp.com/app/tramites/transito/permiso_de_circulacion", "content": "Sacar el permiso del auto, papeles del vehículo, patente del auto, traslado de permiso de otra comuna, revisión técnica y seguro soap."},
            {"title": "Pago Permiso de Circulación", "cat": "Tránsito", "url": "https://pago.smc.cl/pagoPCVv2/muni/lo_barnechea.aspx", "content": "Pagar la patente online, botón de pago permiso de circulación, cuotas del permiso de auto, pago patente vehicular."},

            # 2. PATENTES
            {"title": "Patentes Municipales", "cat": "Patentes", "url": "https://mlobarnechea.custhelp.com/app/tramites/patentes_municipales", "content": "Abrir un negocio, patente comercial, permiso para trabajar, patente profesional, vender alcohol, botillería, pago semestral patentes comerciales."},
            {"title": "Patente Microempresa Familiar", "cat": "Patentes", "url": "https://mlobarnechea.custhelp.com/app/answers/detail/a_id/93", "content": "Negocio en la casa, emprendimiento familiar, pyme en el hogar, formalizar negocio casero, ley microempresa familiar MEF."},
            {"title": "Publicidad y Propaganda", "cat": "Patentes", "url": "https://mlobarnechea.custhelp.com/app/answers/detail/a_id/94", "content": "Poner un letrero, publicidad en la calle, carteles comerciales, aviso en local, derechos de publicidad."},

            # 3. OBRAS (DOM)
            {"title": "Certificados DOM Online", "cat": "Obras", "url": "https://lobarnechea.filedom.cl/index.php?parent=Direcci%C3%B3n%20de%20Obras%20Municipales", "content": "Certificado de número, informaciones previas CIP, zonificación de mi casa, papeles de la dirección de obras, ley de urbanismo."},
            {"title": "Edificación y Urbanización", "cat": "Obras", "url": "https://mlobarnechea.custhelp.com/app/dom/inicio", "content": "Permiso de construcción, ampliar la casa, planos, formularios técnicos DOM, obras de construcción, recepción definitiva."},

            # 4. JUZGADO (JPL)
            {"title": "Juzgado de Policía Local", "cat": "JPL", "url": "https://mlobarnechea.custhelp.com/app/jpl/inicio", "content": "Hacer una denuncia, juzgado local, citación al juez, problemas con vecinos, ley del consumidor, tribunal local."},
            {"title": "Causas de Choque e Indagatorias", "cat": "JPL", "url": "https://mlobarnechea.custhelp.com/app/answers/detail/a_id/77/incidents.c$tipo_atencion/221", "content": "Me chocaron el auto, demanda por choque, accidente de tránsito, pelea por choque, daños de vehículo, denuncia por colisión."},
            {"title": "Pago de Multas y Tag", "cat": "JPL", "url": "https://pago.smc.cl/pagoRMNPv2/muni/lo_barnechea.aspx", "content": "Pagar un parte, multa de tránsito, pagar el tag, deuda judicial, infracción empadronada, multas de caminos y autopistas."},

            # 5. PAGOS Y SERVICIOS VARIOS
            {"title": "Derecho de Aseo Domiciliario", "cat": "Pagos", "url": "https://pago.smc.cl/pagoASEOv2/muni/lo_barnechea.aspx", "content": "Pagar basura, cobro derecho de aseo domiciliario, pagar aseo casa, deuda de aseo municipal, pagar retiro de residuos sólidos, boleta de aseo."},
            {"title": "Contribuciones", "cat": "Pagos", "url": "https://www.tgr.cl/pagos/pago-de-contribuciones/", "content": "Pago de contribuciones, impuesto territorial, deuda de bienes raíces, tesorería general de la república, impuesto a la propiedad."},
            {"title": "Retiro de Escombros y Ramas", "cat": "Aseo", "url": "https://pago.smc.cl/pagoVARIOSv2/muni/lo_barnechea.aspx", "content": "Sacar ramas de la casa, retiro de escombros, cachureos, basura de construcción, limpiar el patio, retiro voluminosos."},

            # 6. SOCIAL Y COMUNIDAD
            {"title": "Beneficios y Subvenciones", "cat": "Social", "url": "https://mlobarnechea.custhelp.com/app/postulaciones/inicio/a_id/47", "content": "Ayuda económica, subsidio, registro social de hogares, becas escolares, ayuda social, vulnerabilidad, asistencia social."},
            {"title": "Deporte y Cultura", "cat": "Comunidad", "url": "https://lobarnechea.saltala.com/#/servicios/unit-506", "content": "Talleres deportivos, gimnasio, clases de cultura, cursos de deporte, eventos municipales, actividades extracurriculares."},
            {"title": "Club Preferente", "cat": "Comunidad", "url": "https://mlobarnechea.custhelp.com/app/club_preferente", "content": "Tarjeta vecino, beneficios club preferente, descuentos para vecinos, tarjeta municipal, convenio club preferente."},
            {"title": "Zoonosis y Mascotas", "cat": "Salud", "url": "https://lobarnechea.saltala.com/#/servicios/unit-462", "content": "Veterinario, vacunas perro o gato, esterilización, perrito enfermo, tenencia responsable, chip mascotas, clínica veterinaria municipal."},

            # 7. SALUD Y SEGURIDAD
            {"title": "Farmacia Comunal", "cat": "Salud", "url": "https://mlobarnechea.custhelp.com/app/answers/detail/a_id/54", "content": "Remedios baratos, comprar medicamentos, inscripción farmacia municipal, remedios por receta, botica comunal."},
            {"title": "Programa Más Salud", "cat": "Salud", "url": "https://lobarnechea.cl/vecinos/salud/mas-salud/", "content": "Me siento mal, médico a domicilio, doctor en casa, visita médica, atención de salud al hogar, enfermero a domicilio, atención médica domiciliaria."},
            {"title": "Emergencias 1405", "cat": "Seguridad", "url": "https://lobarnechea.cl/seguridad/telefono-de-emergencias-1405/", "content": "Llamar a seguridad, número de emergencia, me robaron, accidente urgente, 1405, auxilio, seguridad ciudadana."},
            {"title": "Encarga tu Casa", "cat": "Seguridad", "url": "https://lobarnechea.cl/seguridad/encarga-tu-casa/", "content": "Voy a viajar y dejo la casa sola, vigilar mi casa por vacaciones, encargar mi hogar a seguridad, vigilancia casa sola."},
            {"title": "Atención a Víctimas", "cat": "Seguridad", "url": "https://lobarnechea.cl/seguridad/atencion-a-victimas/", "content": "Fui víctima de un robo, asalto, ayuda legal por delito, apoyo psicológico por robo, defensa a víctimas."},

            # 8. MUNICIPALIDAD
            {"title": "Audiencias con el Alcalde", "cat": "Muni", "url": "https://lobarnechea.cl/audiencias-con-el-alcalde/", "content": "Hablar con el alcalde, pedir audiencia, ley de lobby, cita con la autoridad municipal, reunión alcalde."},
            {"title": "Participación Ciudadana", "cat": "Muni", "url": "https://tudecides.lobarnechea.cl/", "content": "Votar proyectos, consultas ciudadanas, opinar sobre la comuna, plebiscitos locales, presupuestos participativos."},
            {"title": "Inscripción al Concejo", "cat": "Muni", "url": "https://mlobarnechea.custhelp.com/ci/documents/detail/5/27/12/7886d3466d6475cfc0287d77dfac9d648da75a8c", "content": "Ir a la reunión del concejo municipal, participar en sesión del concejo, hablar en el concejo, audiencia concejo."},
            {"title": "Estado de Solicitud", "cat": "Muni", "url": "https://mlobarnechea.custhelp.com/app/estado_solicitudes", "content": "Cómo va mi trámite, revisar solicitud, número de ingreso, ver seguimiento de trámite, consulta estado expediente."}
        ]

        for item in data_to_load:
            print(f"⌛ Procesando: {item['title']}...")
            embedding = generate_embedding(item["content"])
            
            nuevo_doc = Document(
                title=item["title"],
                content=item["content"],
                url=item["url"],
                category=item["cat"],
                embedding=embedding
            )
            db.add(nuevo_doc)
        
        print("💾 Guardando cambios en la base de datos...")
        db.commit()
        
        count = db.query(Document).count()
        print(f"✨ ¡Éxito! Total de registros ahora: {count}")

    except Exception as e:
        db.rollback()
        print(f"❌ ERROR CRÍTICO: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_data_final()