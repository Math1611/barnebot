from services.vector_service import search_vector_database
import os
from google import genai
from dotenv import load_dotenv
from services.ai_service import AIService

ai_handler = AIService()
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class RAGService:
    async def process_query(self, db, query_text, user_lang="es"):
        response = await ai_handler.generate_with_context(query_text, context, user_lang)
        results = search_vector_database(db, query_text)

        if results and results[0].similarity > 0.25:
            context = "\n".join([f"- {r.title}: {r.url} ({r.content})" for r in results[:3]])

        if not results:
            return ("¡Pucha! No pillé info específica sobre eso en mi base de datos municipal. 😅\n\n"
                    "Prueba con otras palabras o escribe *menu* para ver las opciones principales. ¡Aquí estoy para apañar!")
        
        
        context = "\n".join([f"- {r.title}: {r.content} (Link: {r.url})" for r in results])
        
        prompt = f"""
        Eres 'BarneBot', el asistente oficial de la Municipalidad de Lo Barnechea 🏡.
        
        REGLA DE ORO DE IDIOMA:
        1. Responde SIEMPRE en el mismo idioma en que te escribe el vecino ({user_lang}). 
        2. Si te escriben en inglés, tu respuesta debe ser en inglés fluido y amable.
        3. Los links y nombres de departamentos (como 'Juzgado de Policía Local') mantenlos en su nombre original pero explica qué son.
        4. Si el vecino pregunta por el 'Estado de su solicitud', envíalo a: https://mlobarnechea.custhelp.com/app/estado_solicitudes
        5. Cuando el usuario se pone en contexto de ingles, traduce el contenido del RAG al inglés, pero mantén los nombres de departamentos y links en su idioma original (ej: 'Juzgado de Policía Local' sigue igual, pero explicas que es el local police court).
        
        OJO: El vecino puede tener errores de ortografía o tildes (ej: 'musica' por 'música'). 
        Tu primer paso es interpretar qué quiso decir realmente basándote en el CONTEXTO MUNICIPAL.

        CONTEXTO MUNICIPAL:
        {context}
        
        PREGUNTA DEL VECINO:
        {query_text}
        
        RESPUESTA DE BARNEBOT:
        """

        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            return response.text
            
        except Exception as e:
            mejor = results[0]
            if mejor.similarity > 0.45:
                if user_lang == "en":
                    return (
                        f"I found the direct link you were looking for 😁:\n\n"
                        f"📍 *{mejor.title}*\n🔗 {mejor.url}\n\n"
                        f"Hope this helps! I'm here if you need anything else. "
                        f"If I made a mistake, let me know so I can improve! 😋"
                    )
                else:
                    return (
                        f"Encontré el link directo que buscaba 😁:\n\n"
                        f"📍 *{mejor.title}*\n🔗 {mejor.url}\n\n"
                        f"¡Ojalá le sirva! Si necesita otra cosa, aquí estoy. "
                        f"Si me equivoqué, avíseme para mejorar. 😋"
                    )

            if user_lang == "en":
                return "Sorry, I'm having some technical issues. Could you please try again in a moment? 🥖"
            return "Pucha vecino, no entendí mucho lo que quizo decir 🥺 ¿Me lo puede repetir? 🥖"