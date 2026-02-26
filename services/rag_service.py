from services.vector_service import search_vector_database
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Cliente para la respuesta final (Gemini)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class RAGService:
    async def process_query(self, db, query_text: str):
        # 1. Buscamos en los enrutadores del PDF
        results = search_vector_database(db, query_text, threshold=0.2)

        if not results:
            return ("¡Pucha! No pillé info específica sobre eso en mi base de datos municipal. 😅\n\n"
                    "Prueba con otras palabras o escribe *menu* para ver las opciones principales. ¡Aquí estoy para apañar!")

        # 2. Construimos el contexto con la data real de tu PDF actualizado
        context = "\n".join([f"- {r.title}: {r.content} (Link: {r.url})" for r in results])
        
        # 3. EL NUEVO PROMPT CON PERSONALIDAD (BarneBot)
        prompt = f"""
        Eres 'BarneBot', el asistente oficial de la Municipalidad de Lo Barnechea 🏡.
        Tu tono es cercano, amable y muy chileno-respetuoso. 
        
        INSTRUCCIONES DE RESPUESTA:
        - Saluda brevemente si es la primera interacción.
        - Usa la información del CONTEXTO para responder. No inventes links.
        - Sé directo: al vecino le importa el trámite y el link.
        - ¡Usa emojis para que se vea amigable! (📑, 🚗, ⚖️, 🏥).
        - IMPORTANTE: Si hay un link, ponlo solo una vez y bien claro.
        
        CONTEXTO MUNICIPAL:
        {context}

        PREGUNTA DEL VECINO:
        {query_text}

        RESPUESTA DE BARNEBOT:
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Fallback amigable si falla Gemini (ej. error 429)
            mejor = results[0]
            return (f"¡Hola! Tenemos harta demanda ahora, pero te adelanto la info: \n\n"
                    f"📍 *{mejor.title}*\n🔗 Pínchalo aquí: {mejor.url}\n\n"
                    f"¡Espero que te sirva! 😊")