import google.generativeai as genai
import os

class AIService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    async def generate_with_context(self, question: str, context: str, user_lang: str = "es"):
        try:
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
            prompt = (
                f"Eres BarneBot, el asistente amable de la Municipalidad de Lo Barnechea 🏡. "
                f"Responde de forma cercana en {user_lang}. "
                f"Usa este CONTEXTO para responder: {context}. "
                f"Pregunta del vecino: {question}"
                f"Si no sabes la respuesta, di que no la tienes pero que puedes ayudar con otras cosas. No inventes respuestas. Si el contexto no es suficiente, responde que no tienes información suficiente. Siempre mantén un tono amigable y útil."
                f"cuando el usuario pregunte por las becas, RSH, responde con información sobre el Registro Social de Hogares y cómo pueden postular a beneficios sociales. Para eso investiga en https://mlobarnechea.custhelp.com/app/postulaciones/inicio/a_id/47 y le dices cuál está activo en este momento."
            )
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ Error real en AI: {e}")
            return None