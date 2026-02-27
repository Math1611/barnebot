from services.vector_service import search_vector_database
from services.ai_service import AIService

ai_handler = AIService()

class RAGService:
    async def process_query(self, db, query_text, user_lang="es"):
        results = search_vector_database(db, query_text)
        
        if results and results[0].similarity > 0.30:
            mejor = results[0]
            context = "\n---\n".join([f"Trámite: {r.title}\nInfo: {r.content}\nLink: {r.url}" for r in results[:3]])
            
            response = await ai_handler.generate_with_context(query_text, context, user_lang)
            
            if response:
                return response
            
            if user_lang == "en":
                return f"Hi! I found this information for you:\n\n📍 *{mejor.title}*\n🔗 {mejor.url}"
            else:
                return f"¡Hola! Aquí encontré información sobre lo que buscas:\n\n📍 *{mejor.title}*\n🔗 {mejor.url}"

        if user_lang == "en":
            return "I couldn't find exact information. Please try typing the name of the service again."
        return "No encontré información exacta. Por favor, intenta escribir el nombre del trámite nuevamente."