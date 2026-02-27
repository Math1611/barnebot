from google import genai
import os

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    async def generate_with_context(self, question: str, context: str, user_lang: str = "es"):
        system_instruction = f"""
        Eres 'BarneBot', el asistente oficial de la Municipalidad de Lo Barnechea 🏡.
        El vecino ha seleccionado el idioma: {user_lang}. 

        REGLAS DE ORO:
        1. Responde SIEMPRE en el mismo idioma en que te escribe el vecino o el seleccionado ({user_lang}).
        2. Si el vecino pregunta por 'car taxes', se refiere al 'Permiso de Circulación'.
        3. Mantén los nombres de departamentos (ej: 'Juzgado de Policía Local') en original, pero explica qué son en el idioma del usuario.
        4. Si el contexto incluye una URL, proporciónala SIEMPRE de forma clara.
        5. Sé amable y cercano ("vecino/a" o "neighbor").
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                config={"system_instruction": system_instruction},
                contents=f"CONTEXTO MUNICIPAL:\n{context}\n\nPREGUNTA DEL VECINO:\n{question}"
            )
            return response.text
        except Exception as e:
            print(f"❌ Error en AI Service: {e}")
            if user_lang == "en":
                return "I'm sorry, neighbor. I cannot access the municipal database right now. Please try again later."
            return "Lo siento, vecino. En este momento no puedo acceder a la base de datos municipal. Por favor, intente más tarde."