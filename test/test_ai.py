from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- LISTADO DE MODELOS DISPONIBLES ---")
for m in client.models.list():
    if 'embedContent' in m.supported_methods:
        print(f"Modelo para embedding: {m.name}")