from google import genai
import os

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Optimizamos el prompt para el enrutamiento del PDF
        self.system_instruction = """
        Eres el asistente virtual de la Municipalidad de Lo Barnechea.
        Tu misión es guiar al vecino al departamento o trámite correcto.
        
        INSTRUCCIONES:
        1. Usa el CONTEXTO para dar un resumen breve del trámite.
        2. Si el contexto incluye una URL, proporciónala SIEMPRE de forma clara.
        3. Si el vecino pregunta por el 'Estado de su solicitud', envíalo a: https://mlobarnechea.custhelp.com/app/estado_solicitudes
        4. Sé amable y usa un lenguaje cercano ("vecino", "vecina").
        """

    async def generate_with_context(self, question: str, context: str):
        try:
            # CAMBIO: Usamos el nombre de modelo más estable para el SDK
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                config={"system_instruction": self.system_instruction},
                contents=f"CONTEXTO MUNICIPAL:\n{context}\n\nPREGUNTA DEL VECINO:\n{question}"
            )
            return response.text
        except Exception as e:
            # Si da error 404, el log te dirá si el modelo cambió de nombre
            print(f"❌ Error en AI Service: {e}")
            return "Lo siento, vecino. En este momento no puedo acceder a la base de datos municipal. Por favor, intente más tarde."