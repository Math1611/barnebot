import google.generativeai as genai
import os

class AIService:
    def __init__(self):
        # Configuramos la API Key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    async def generate_with_context(self, question: str, context: str, user_lang: str = "es"):
        try:
            # FORZAMOS el modelo gemini-1.5-flash que es el actual
            # Pero lo llamamos de forma que no use v1beta
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
            prompt = (
                f"Eres BarneBot, el asistente amable de la Municipalidad de Lo Barnechea 🏡. "
                f"Responde de forma cercana en {user_lang}. "
                f"Usa este CONTEXTO para responder: {context}. "
                f"Pregunta del vecino: {question}"
            )
            
            # Intentamos generar contenido
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            # Si sigue saliendo el 404, imprimiremos el error exacto
            print(f"❌ Error real en AI: {e}")
            return None